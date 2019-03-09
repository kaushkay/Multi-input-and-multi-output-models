from keras.layers import Input, Embedding, LSTM, Dense
from keras.models import Model
import keras

# Headline input: meant to receive sequences of 100 integers, between 1 and 10000.
# Note that we can name any layer by passing it a "name" argument.
main_input = Input(shape=(100,), dtype='int32', name='main_input')

# This embedding layer will encode the input sequence
# into a sequence of dense 512-dimensional vectors.
x = Embedding(output_dim=512, input_dim=1000, input_length=100)(main_input)

# A LSTM will transform the vector sequence into a single vector,
# containing information about the entire sequence
lstm_out = LSTM(32)(x)

auxiliary_output = Dense(1, activation='sigmoid', name='aux_output')(lstm_out)

auxiliary_input = Input(shape=(5,), name='aux_input')
x = keras.layers.concatenate([lstm_out, auxiliary_input])

# We stack a deep densely-connected network on top
x = Dense(64, activation='relu')(x)
x = Dense(64, activation='relu')(x)
x = Dense(64, activation='relu')(x)

# And finally we add the main logistic regression layer
main_output = Dense(1, activation='sigmoid', name='main_output')(x)


model = Model(inputs=[main_input, auxiliary_input], outputs=[main_output, auxiliary_output])

model.compile(optimizer='rmsprop', loss='binary_crossentropy', loss_weights=[1.0,0.2])

# Since our inputs and outputs are named (we passed them a "name" argument),
# we could also have compiled the model via:

#model.compile(optimizer='rmsprop',
#              loss={'main_output': 'binary_crossentropy', 'aux_output': 'binary_crossentropy'},
#              loss_weights={'main_output': 1., 'aux_output': 0.2})

# And trained it via:
#model.fit({'main_input': headline_data, 'aux_input': additional_data},
#          {'main_output': labels, 'aux_output': labels},
#          epochs=50, batch_size=32)
