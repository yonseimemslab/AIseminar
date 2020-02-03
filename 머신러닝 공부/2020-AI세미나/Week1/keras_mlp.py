# Multilayer Perceptron (MLP) 생성

model = Sequential()

# Dense(256)의 의미는 256개의 hidden unit을 가지는 fully connected layer
# keras에서는 첫 번째 Layer, 즉 input layer의 input dimension만 지정하면
# 뒤의 연결되는 Layer의 dimension은 간단하게 작성 가능하다.

# width * height = 784인 dimension
# glorot_uniform == Xavier Initialization, keras에서는 내부적으로 이미 제공
# 그 외 he_uniform 등도 이미 구현되어있다.

# 첫 번째 Layer (Input layer)
model.add(Dense(256, input_dim=width * height, init='glorot_uniform', activation='relu'))
model.add(Dropout(0.3))        # 30% 정도를 Drop

# 두 번째 Layer (Hidden layer 1)
# 두 번째 Layer부터는 output_dim만 설정하면 된다
# input_dim은 이전 레이어의 output_dim과 같다고 가정함
model.add(Dense(256, init='glorot_uniform', activation='relu'))
model.add(Dropout(0.3))

# 세 번째 Layer (Hidden layer 2)
model.add(Dense(256, init='glorot_uniform', activation='relu'))
model.add(Dropout(0.3))

# 네 번째 Layer (Hidden layer 3)
model.add(Dense(256, init='glorot_uniform', activation='relu'))
model.add(Dropout(0.3))

# 다섯 번째 Layer (Output layer)
# Output layer는 softmax activation function
number_of_class = 10  # MNIST 예제는 10가지의 Category를 가지고 있다.
model.add(Dense(number_of_class, activation='softmax'))

# Cost function 및 Optimizer 설정
# Multiclass 분류이므로 Cross-entropy 사용
# Adam optimizer 사용
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# model training
training_epochs = 15
batch_size = 100
model.fit(X_train, y_train, nb_epoch=training_epochs, batch_size=batch_size)

# Model evaluation using test set
print('모델 평가')
evaluation = model.evaluate(X_test, y_test, batch_size=batch_size)
print('Accuracy: ' + str(evaluation[1]))
