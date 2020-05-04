/**
    The module to bind C into Python.
    For introduction and explanations about the notation
    see the tutorial at http://adamlamers.com/post/NUBSPFQJ50J1
    (c)2017 Mihkel Veske
*/
#include <Python.h>

#include <stdio.h>
#include <sys/types.h>
#include <string.h>
#include <termios.h>
#include <sys/ioctl.h>
#include <sys/types.h>
#include <unistd.h>
#include <stdlib.h>

#include <libusbdrdaq-1.0/usbDrDaqApi.h>
#include <libusbdrdaq-1.0/PicoStatus.h>

#define Sleep(a) usleep(1000*a)
#define max(a,b) ((a) > (b) ? a : b)
#define min(a,b) ((a) < (b) ? a : b)
#define TRUE		1
#define FALSE		0

short g_handle;
PICO_STATUS status;

// Calculate the average for the dataset
short average(uint32_t nSamples, short* samples){
    unsigned long i;
    long sum = 0;
    for(i = 0; i < nSamples; ++i)
        sum += (long) samples[i];
    
    return sum / nSamples;
}

// Get single data point from "channel"
short get_data(USB_DRDAQ_INPUTS channel) {
    short value;
    unsigned short overflow;
    UsbDrDaqGetSingle(g_handle, channel, &value, &overflow);
    return value;
}

// Get "nSamples" data points from the data in "channel" within time period of "msForBlock"
short* get_data_block(USB_DRDAQ_INPUTS channel, uint32_t nSamples, uint32_t msForBlock) {
	uint32_t  usForBlock = msForBlock * 1000;
	unsigned short overflow;
	uint32_t triggerIndex = 0;
    short nChannels = 1;
        
    short* samples;
    samples = (short*) malloc(nSamples * sizeof(short));

	//Set the trigger (disabled)
	status = UsbDrDaqSetTrigger(g_handle, FALSE, 0, 0, 0, 0, 0, 0, 0);
	//set sampling rate and channels
	status = UsbDrDaqSetInterval(g_handle, &usForBlock, nSamples, &channel, nChannels);
    //Start streaming
    status = UsbDrDaqRun(g_handle, nSamples, BM_SINGLE);
    //Wait until unit is ready
    short isReady = 0;
    while(isReady == 0)
        status = UsbDrDaqReady(g_handle, &isReady);

    status = UsbDrDaqGetValues(g_handle, samples, &nSamples, &overflow, &triggerIndex);
    status = UsbDrDaqStop(g_handle);
    
    return samples;
}

/* Make single light measurement */
static PyObject* py_get_light(PyObject* self, PyObject* args) {
    short value = get_data(USB_DRDAQ_CHANNEL_LIGHT);
    double light = value / 10.0;
    return Py_BuildValue("d", light);
}

/* Make single temperature measurement */
static PyObject* py_get_temperature(PyObject* self, PyObject* args) {
    short value = get_data(USB_DRDAQ_CHANNEL_TEMP);
    double temperature = value / 10.0;
    return Py_BuildValue("d", temperature);
}

/* Make single temperature measurement with the probe */
static PyObject* py_get_ext1(PyObject* self, PyObject* args) {
    short value = get_data(USB_DRDAQ_CHANNEL_EXT1);
    double ext1 = value / 10.0;
    return Py_BuildValue("d", ext1);
}

/* Make single non-averaged pH measurement */
static PyObject* py_get_pH_real(PyObject* self, PyObject* args) {
    short value = get_data(USB_DRDAQ_CHANNEL_PH);
    double ph = value / 100.0;
    return Py_BuildValue("d", ph);
}

/* Make single averaged pH measurement */
static PyObject* py_get_pH(PyObject* self, PyObject* args) {
    uint32_t msForBlock = 200;
    uint32_t nSamples = 1000;
    short* samples;
    
    samples = get_data_block(USB_DRDAQ_CHANNEL_PH, nSamples, msForBlock);
    short value = average(nSamples, samples);

    double pH = value / 100.0;
    return Py_BuildValue("d", pH);
}

static PyObject* py_set_output(PyObject* self, PyObject* args) {
    int channel, state;
    if (!PyArg_ParseTuple(args, "ii", &channel, &state))
        return NULL;
    if (channel >= 1 && channel <= 4)
        if (state)
            UsbDrDaqSetDO(g_handle, channel, 1);
        else
            UsbDrDaqSetDO(g_handle, channel, 0);
        
    return Py_BuildValue("s", "0");
}

static PyObject* py_set_pwm(PyObject* self, PyObject* args) {
    unsigned short period = 1000; // 0-65535

    int channel, cycle;
    if (!PyArg_ParseTuple(args, "ii", &channel, &cycle))
        return NULL;
    if (channel >= 1 && channel <= 4 && cycle >= 0 && cycle <= 100)
        UsbDrDaqSetPWM(g_handle, channel, period, cycle);
        
    return Py_BuildValue("s", "0");
}

static PyObject* py_set_led(PyObject* self, PyObject* args) {
    int red, green, blue;
    if (!PyArg_ParseTuple(args, "iii", &red, &green, &blue))
        return NULL;
    if (red >= 0 && red <= 255 && green >= 0 && green <= 255 && blue >= 0 && blue <= 255)
        UsbDrDaqSetRGBLED(g_handle, (unsigned int)red, (unsigned int)green, (unsigned int)blue);

    return Py_BuildValue("s", "0");
}
            
static PyObject* py_led_on(PyObject* self, PyObject* args) {
	unsigned short red = 255;
    unsigned short green = 255;
    unsigned short blue = 255;
    UsbDrDaqSetRGBLED(g_handle, red, green, blue);

    return Py_BuildValue("s", "0");
}

static PyObject* py_led_off(PyObject* self, PyObject* args) {   
    UsbDrDaqSetRGBLED(g_handle, 0, 0, 0);
    return Py_BuildValue("s", "0");
}

static PyObject* py_led_blink(PyObject* self, PyObject* args) {
	py_led_on(self, args);
    Sleep(50);
    py_led_off(self, args);
    return Py_BuildValue("s", "0");
}

static PyObject* py_init_drdaq(PyObject* self, PyObject* args) {
    UsbDrDaqEnableRGBLED(g_handle, 1);
    return Py_BuildValue("s", "0");
}

static PyObject* py_close_drdaq(PyObject* self, PyObject* args) {
    UsbDrDaqCloseUnit(g_handle);
    return Py_BuildValue("s", "0");
}

/* Bind Python function names to C functions */
static PyMethodDef drdaq_methods[] = {
    {"init", py_init_drdaq, METH_VARARGS},
    {"close", py_close_drdaq, METH_VARARGS},
    {"get_light", py_get_light, METH_VARARGS},
    {"get_temperature", py_get_temperature, METH_VARARGS},
    {"get_ext1", py_get_ext1, METH_VARARGS},
    {"get_pH", py_get_pH, METH_VARARGS},
    {"get_pH_real", py_get_pH_real, METH_VARARGS},
    {"led_on", py_led_on, METH_VARARGS},
    {"led_off", py_led_off, METH_VARARGS},
    {"led_blink", py_led_blink, METH_VARARGS},
    {"set_output", py_set_output, METH_VARARGS},
    {"set_pwm", py_set_pwm, METH_VARARGS},
    {"set_led", py_set_led, METH_VARARGS},
    {NULL, NULL}
};

// Module definition for Python 3
static struct PyModuleDef drdaq_definition = { 
    PyModuleDef_HEAD_INIT,
    "drdaq",
    "Python module with DrDAQ drivers",
    -1, 
    drdaq_methods
};

// Module initialization in Python 3
PyMODINIT_FUNC PyInit_drdaq(void) {
    Py_Initialize();
    PICO_STATUS status = UsbDrDaqOpenUnit(&g_handle);
	if (status != 0)
		printf ("Unable to open DrDAQ!\n");
    return PyModule_Create(&drdaq_definition);
}

/* Python2 calls this to initialize the module */
/*
void initdrdaq(void) {
    (void) Py_InitModule("drdaq", drdaq_methods);

    PICO_STATUS status = UsbDrDaqOpenUnit(&g_handle);
	if (status != 0)
		printf ("Unable to open DrDAQ!\n");
}
*/
