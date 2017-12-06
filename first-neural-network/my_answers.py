import numpy as np


class NeuralNetwork(object):
    def __init__(self, input_nodes, hidden_nodes, output_nodes, learning_rate):
        # Set number of nodes in input, hidden and output layers.
        self.input_nodes = input_nodes
        self.hidden_nodes = hidden_nodes
        self.output_nodes = output_nodes

        # Initialize weights
        self.weights_input_to_hidden = np.random.normal(0.0, self.input_nodes**-0.5, 
                                       (self.input_nodes, self.hidden_nodes))

        self.weights_hidden_to_output = np.random.normal(0.0, self.hidden_nodes**-0.5, 
                                       (self.hidden_nodes, self.output_nodes))
        self.lr = learning_rate
        
        #### TODO: Set self.activation_function to your implemented sigmoid function ####
        #
        # Note: in Python, you can define a function with a lambda expression,
        # as shown below.
        self.activation_function = lambda x : 1 / (1 + np.exp(-x))  # Replace 0 with your sigmoid calculation.
        
        ### If the lambda code above is not something you're familiar with,
        # You can uncomment out the following three lines and put your 
        # implementation there instead.
        #
        #def sigmoid(x):
        #    return 0  # Replace 0 with your sigmoid calculation here
        #self.activation_function = sigmoid
                    

    def train(self, features, targets):
        ''' Train the network on batch of features and targets. 
        
            Arguments
            ---------
            
            features: 2D array, each row is one data record, each column is a feature
            targets: 1D array of target values
        
        '''
        n_records = features.shape[0]
        delta_weights_i_h = np.zeros(self.weights_input_to_hidden.shape)
        delta_weights_h_o = np.zeros(self.weights_hidden_to_output.shape)
        for X, y in zip(features, targets):
            
            final_outputs, hidden_outputs = self.forward_pass_train(X)  # Implement the forward pass function below
            # Implement the backproagation function below
            delta_weights_i_h, delta_weights_h_o = self.backpropagation(final_outputs, hidden_outputs, X, y, 
                                                                        delta_weights_i_h, delta_weights_h_o)
        self.update_weights(delta_weights_i_h, delta_weights_h_o, n_records)


    def forward_pass_train(self, X):
        ''' Implement forward pass here 
         
            Arguments
            ---------
            X: features batch

        '''
        #### Implement the forward pass here ####
        ### Forward pass ###
        # TODO: Hidden layer - Replace these values with your calculations.

        ## From Backpropagation lab forward pass code reference
        # hidden_input = np.dot(x, weights_input_hidden)
        # hidden_output = sigmoid(hidden_input)
        # output = sigmoid(np.dot(hidden_output, weights_hidden_output))

        hidden_inputs = np.dot(X, self.weights_input_to_hidden) # signals into hidden layer
        hidden_outputs = self.activation_function(hidden_inputs) # signals from hidden layer

        # TODO: Output layer - Replace these values with your calculations.
        final_inputs = np.dot(hidden_outputs, self.weights_hidden_to_output) # signals into final output layer
        #final_outputs = self.activation_function(final_inputs) # signals from final output layer
        final_outputs = final_inputs # signals from final output layer
        
        return final_outputs, hidden_outputs

    def backpropagation(self, final_outputs, hidden_outputs, X, y, delta_weights_i_h, delta_weights_h_o):
        ''' Implement backpropagation
         
            Arguments
            ---------
            final_outputs: output from forward pass
            y: target (i.e. label) batch
            delta_weights_i_h: change in weights from input to hidden layers
            delta_weights_h_o: change in weights from hidden to output layers

        '''
        #### Implement the backward pass here ####
        ### Backward pass ###

        ## From backprop lab code
        # error = y - output
        # output_error_term = error * output * (1-output)
        # hidden_error = np.dot(output_error_term, weights_hidden_output)
        # hidden_error_term = hidden_error * hidden_output * (1 - hidden_output)
        # del_w_hidden_output += output_error_term * hidden_output
        # del_w_input_hidden += hidden_error_term * x[:,None]
        
 
        
        # TODO: Output error - Replace this value with your calculations.
        error = y - final_outputs # Output layer error is the difference between desired target and actual output.
        #print("error: ", error) 
        
        # TODO: Backpropagated error term - Replace these values with your calculations.
        #output_error_term = error * final_outputs * (1-final_outputs)
        output_error_term = error # removed final_outputs * (1-final_outputs) since we are linear instead of sigmoid

        #print("output_error_term: ", output_error_term) 

        # TODO: Calculate the hidden layer's contribution to the error
        # print("output_error_term.shape: ",output_error_term.shape)
        # print("self.weights_hidden_to_output.T.shape: ",self.weights_hidden_to_output.T.shape)
        hidden_error = np.dot(output_error_term, self.weights_hidden_to_output.T)
        #print("hidden_error: ", hidden_error) 
        
        # TODO: Backpropagated hidden error term - Replace these values with your calculations.
        hidden_error_term = hidden_error * hidden_outputs * (1-hidden_outputs)
        #print("hidden_error_term: ", hidden_error_term) 
        #print("   hidden_outputs:", hidden_outputs)
        
        # Weight step (input to hidden)
        delta_weights_i_h += hidden_error_term * X[:,None]
        #print("delta_weights_i_h: ", delta_weights_i_h) 
        #print("     hidden_error_term: ", hidden_error_term) 
        #print("     X[:,None]: ", X[:,None]) 
        
        
        # Weight step (hidden to output)
        #print("output_error_term.shape: ",output_error_term.shape)
        #print("output_error_term[:,None].shape: ",output_error_term[:,None].shape)
        #print("output_error_term.T.shape: ",output_error_term.T.shape)
        #print("hidden_outputs.shape: ",hidden_outputs.shape)
        #print("hidden_outputs[:,None].shape: ",hidden_outputs[:,None].shape)
        #print("hidden_outputs.T.shape: ",hidden_outputs.T.shape)
        #print("delta_weights_h_o.shape: ",delta_weights_h_o.shape)
        delta_weights_h_o += hidden_outputs[:,None] * output_error_term
        
        #print("delta_weights_h_o: ", delta_weights_i_h) 
        #print("     hidden_outputs[:,None]: ", hidden_outputs[:,None]) 
        #print("     output_error_term: ", output_error_term) 
        
        return delta_weights_i_h, delta_weights_h_o

    def update_weights(self, delta_weights_i_h, delta_weights_h_o, n_records):
        ''' Update weights on gradient descent step
         
            Arguments
            ---------
            delta_weights_i_h: change in weights from input to hidden layers
            delta_weights_h_o: change in weights from hidden to output layers
            n_records: number of records

        '''
        ## From backprop lab code
        # weights_input_hidden += learnrate * del_w_input_hidden / n_records
        # weights_hidden_output += learnrate * del_w_hidden_output / n_records
 

        self.weights_hidden_to_output += self.lr * delta_weights_h_o / n_records # update hidden-to-output weights 
        self.weights_input_to_hidden += self.lr * delta_weights_i_h / n_records # update input-to-hidden weights 

    def run(self, features):
        ''' Run a forward pass through the network with input features 
        
            Arguments
            ---------
            features: 1D array of feature values
        '''

        #### Implement the forward pass here ####
        # TODO: Hidden layer - replace these values with the appropriate calculations.
        hidden_inputs = np.dot(features, self.weights_input_to_hidden) # signals into hidden layer
        hidden_outputs = self.activation_function(hidden_inputs) # signals from hidden layer
        
        # TODO: Output layer - Replace these values with the appropriate calculations.
        final_inputs = np.dot(hidden_outputs, self.weights_hidden_to_output) # signals into final output layer
        final_outputs = final_inputs # signals from final output layer 
        
        return final_outputs


#########################################################
# Set your hyperparameters here
##########################################################
iterations = 100
learning_rate = 0.1
hidden_nodes = 2
output_nodes = 1
