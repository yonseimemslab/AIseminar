import numpy as np
import sys

class NeuralNetMLP(object):
    """
    *용어 정리 및 initializer에 관한 설명*
    n_hidden : int( default : 30 )
    l2 :float ( default : 0 ) --> l2규제 구현 0일 경우 제한 없음 l2 규제 람다 값
    epoch : int ( default : 100 )
    eta : float ( default : 0.001 ) learning rate임
    shuffle : bool ( default : True )
    minibatch_size : int ( default : 1 )
    seed : int (default : none) 랜덤 난수 형성 시드
    eval_ : dict -->훈련비용, 정확도, 검증 정확도 수집용 딕셔너리
    """
    def __init__(self,n_hidden=30,l2=0.,epochs=100,eta=0.001,shuffle=True,minibatch_size=1,seed=None):
        self.random=np.random.RandomState(seed)
        self.n_hidden=n_hidden
        self.l2=l2
        self.epochs=epochs
        self.eta=eta
        self.shuffle=shuffle
        self.minibatch_size=minibatch_size

    def _onehot(self,y,n_classes):
        """
        순서의 특성이 없는 정보를 가지고 기계적으로 학습을 하기 위해서 수치화를 하는 방법임.
        e.g) 색을 rbg로 표현을 할 경우, 숫자간의 차이로 인해서 읽어들이는 값의 정확한 상관관계 추론이 힘들어진다.
        이러한 문제를 막기 위해서 onehot encoder는 데이터의 특성을 별도의 행을 추가를 해서 dummy정보를 생성

        y: 배열, 크기 = [n_sample] --> 타겟값
        onehot : 배열, 크기 =(n_samples,n_labels)
        """
        onehot=np.zeros((n_classes,y.shape[0]))
        for idx, val in enumerate(y.astype(int)):
            onehot[val,idx]=1
        return onehot.T

    def _sigmoid(self,z):
        return 1./(1.+np.exp(-np.clip(z,-250,250)))

    def _forward(self,X):
        """
        단계1. 은닉층의 weight와 bias 계산
            n_sample(n개의 데이터)*n_feature(n개의 입력값) dot n_feature(n개의 입력값)*n_hidden(은닉층의 뉴런수) = n_samples,n_hidden
        """

        z_h=np.dot(X,self.w_h)+self.b_h

        """
        단계2. 은닉층에서 계산된 weight와 bias를 활성화 함수를 통해서 계산
            활성화 함수로는 시그모이드 함수를 사용.
        """

        a_h=self._sigmoid(z_h)

        """
        단계3. 출력층의 최종 입력
            n_sample*n_hidden dot n_hidden*n_class = n_samples,n_class_label
        """

        z_out=np.dot(a_h,self.w_out)+self.b_out

        """
        단계4. 출력층의 활성화 출력
            시그모이드 함수
        """

        a_out=self._sigmoid(z_out)

        return z_h,a_h,z_out,a_out

    def _compute_cost(self,y_enc,output):
        """
        y_enc: 배열, 크기 = n_sample*n_label
        output: 배열, 크기 = n_sample*n_output_unit
        cost: float--> 규제가 포함된 비용
        """

        L2_term=(self.l2*(np.sum(self.w_h**2.)+np.sum(self.w_out**2.)))
        term1=-y_enc*(np.log(output))
        term2=(1.-y_enc)*np.log(1.-output)
        cost=np.sum(term1-term2)+L2_term
        return cost

    def predict(self,X):
        """
        X:배열, 크기=n_sample*n_feature-->원본의 특성을 입력(입력값)
        y_pred:배열, 크기=n_sample*n_output_feature --> 결과값
        """

        z_h, a_h, z_out, a_out=self._forward(X)
        y_pred=np.argmax(z_out,axis=1)
        return y_pred

    def fit(self,X_train,y_train,X_valid,y_valid):
        n_output=np.unique(y_train).shape[0]
        n_features=X_train.shape[1]

        """
        가중치 초기화
            1. 은닉층 사이의 가중치 초기화
            2. 출력층 사이의 가중치 초기화
        """

        self.b_h=np.zeros(self.n_hidden)
        self.w_h=self.random.normal(loc=0.0,scale=0.1,size=(n_features,self.n_hidden))


        self.b_out=np.zeros(n_output)
        self.w_out=self.random.normal(loc=0.0,scale=0.1,size=(self.n_hidden,n_output))


        epoch_strlen=len(str(self.epochs))
        self.eval_={'cost':[],'train_acc':[],'valid_acc':[]}

        y_train_enc=self._onehot(y_train,n_output)

        """
        epoch에 따른 훈련 반복
        """

        for i in range(self.epochs):
            indices=np.arange(X_train.shape[0])

            if self.shuffle:
                self.random.shuffle(indices)

            for start_idx in range(0,indices.shape[0]-self.minibatch_size+1,self.minibatch_size):
                batch_idx=indices[start_idx:start_idx+self.minibatch_size]

                z_h,a_h,z_out,a_out=self._forward(X_train[batch_idx])

                """
                Backpropagation
                """
                sigma_out=a_out-y_train_enc[batch_idx]
                sigmoid_derivative_h=a_h*(1.-a_h)
                sigma_h=(np.dot(sigma_out,self.w_out.T)*sigmoid_derivative_h)

                grad_w_h=np.dot(X_train[batch_idx].T,sigma_h)
                grad_b_h=np.sum(sigma_h,axis=0)

                grad_w_out=np.dot(a_h.T,sigma_out)
                grad_b_out=np.sum(sigma_out,axis=0)


                delta_w_h=(grad_w_h+self.l2*self.w_h)
                delta_b_h=grad_b_h
                self.w_h-=self.eta*delta_w_h
                self.b_h-=self.eta*delta_b_h

                delta_w_out=(grad_w_out+self.l2*self.w_out)
                delta_b_out=grad_b_out
                self.w_out-=self.eta*delta_w_out
                self.b_out-=self.eta*delta_b_out

            """
            evaluation
            """
            z_h,a_h,z_out,a_out=self._forward(X_train)

            cost= self._compute_cost(y_enc=y_train_enc,output=a_out)

            y_train_pred=self.predict(X_train)
            y_valid_pred=self.predict(X_valid)

            train_acc=((np.sum(abs(y_train-y_train_pred)/y_train).astype(np.float)/X_train.shape[0]))
            valid_acc=((np.sum(abs(y_valid-y_valid_pred)/y_valid).astype(np.float)/X_valid.shape[0]))

#            train_acc=(abs(y_train-y_train_pred)/y_train)
#            valid_acc=(abs(y_valid-y_valid_pred)/y_valid)

            sys.stderr.write('\r%0*d/%d |비용: %.2f' '|훈련/검증 정확도 : %.2f%% %.2f%%' %(epoch_strlen,i+1,self.epochs,cost,train_acc*100,valid_acc*100))
            sys.stderr.flush()

            self.eval_['cost'].append(cost)
            self.eval_['train_acc'].append(train_acc)
            self.eval_['valid_acc'].append(valid_acc)

        return self
