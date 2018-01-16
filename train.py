import numpy as np
import pickle

def unique(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def softmax(x, temperature):
    exp_x = np.exp(x / temperature)
    return exp_x / np.sum(exp_x)

# RNN
class TextRNN(object):
    def __init__(self, hiddenLayers=300, sequenceLength=50):
        # Hidden Layers
        self.hiddenLayers = hiddenLayers

        # Learning Rate
        self.learningRate = 0.001

        # Hidden State
        self.h = {}

        # Internal cursor
        self.cursor = 0

        # Sequence Length
        self.sequenceLength = sequenceLength

    def train(self, text, ngrams=7, delimiter=" "):
        # Setup delimiter
        self.delimiter = delimiter

        # Split by delimiter
        grams = text.split(delimiter) if delimiter != "" else list(text)

        # Setup Data by Ngrams
        self.data = [delimiter.join(grams[i:i+ngrams]) for i in range(len(grams))[::ngrams]]

        # Get Unique Data
        self.uniqueData = unique(self.data)

        # Get Vocab Maps
        self.indexToGram = {i:gram for i, gram in enumerate(self.uniqueData)}
        self.gramToIndex = {gram:i for i, gram in enumerate(self.uniqueData)}

        # Get vocab size
        self.vocabSize = len(self.uniqueData)

        # Setup Inputs
        inputs = []
        outputs = []
        inputGrams = [self.gramToIndex[gram] for gram in self.data]
        outputGrams = [self.gramToIndex[gram] for gram in self.data[1:]]

        for i, inputGram in enumerate(inputGrams[0:-1]):
            X = np.zeros((self.vocabSize, 1))
            X[inputGram, 0] = 1

            y = np.zeros((self.vocabSize, 1))
            y[outputGrams[i], 0] = 1

            inputs.append(X)
            outputs.append(y)

        self.inputs = inputs
        self.outputs = outputs

        # Input Weights
        self.WXZ = np.random.randn(self.hiddenLayers, self.vocabSize) * 0.1 # Update Gate
        self.WXR = np.random.randn(self.hiddenLayers, self.vocabSize) * 0.1 # Reset Gate
        self.WXC = np.random.randn(self.hiddenLayers, self.vocabSize) * 0.1 # Candidate

        # Hidden Layer Weights
        self.WHZ = np.random.randn(self.hiddenLayers, self.hiddenLayers) * 0.1 # Update Gate
        self.WHR = np.random.randn(self.hiddenLayers, self.hiddenLayers) * 0.1 # Reset Gate
        self.WHC = np.random.randn(self.hiddenLayers, self.hiddenLayers) * 0.1 # Candidate Gate

        # Biases
        self.bC = np.zeros((self.hiddenLayers, 1)) # Candidate Gate
        self.bR = np.zeros((self.hiddenLayers, 1)) # Reset Gate
        self.bZ = np.zeros((self.hiddenLayers, 1)) # Update Gate
        self.bY = np.zeros((self.vocabSize, 1)) # Output

        # Output Layer Weights
        self.WY = np.random.randn(self.vocabSize, self.hiddenLayers) * 0.1

        # Cache for Update
        self.dXZM = np.zeros_like(self.WXZ)
        self.dXRM = np.zeros_like(self.WXR)
        self.dXCM = np.zeros_like(self.WXC)

        self.dHZM = np.zeros_like(self.WHZ)
        self.dHRM = np.zeros_like(self.WHR)
        self.dHCM = np.zeros_like(self.WHC)

        self.dbZM = np.zeros_like(self.bZ)
        self.dbRM = np.zeros_like(self.bR)
        self.dbCM = np.zeros_like(self.bC)

        self.dYM = np.zeros_like(self.WY)

        self.dXZV = np.zeros_like(self.WXZ)
        self.dXRV = np.zeros_like(self.WXR)
        self.dXCV = np.zeros_like(self.WXC)

        self.dHZV = np.zeros_like(self.WHZ)
        self.dHRV = np.zeros_like(self.WHR)
        self.dHCV = np.zeros_like(self.WHC)

        self.dbZV = np.zeros_like(self.bZ)
        self.dbRV = np.zeros_like(self.bR)
        self.dbCV = np.zeros_like(self.bC)

        self.dYV = np.zeros_like(self.WY)


    def forward(self, X, hPrev, temperature=1.0):
        # Update Gate
        zbar = np.dot(self.WXZ, X) + np.dot(self.WHZ, hPrev) + self.bZ
        z = sigmoid(zbar)

        # Reset Gate
        rbar = np.dot(self.WXR, X) + np.dot(self.WHR, hPrev) + self.bR
        r = sigmoid(rbar)

        # Candidate
        cbar = np.dot(self.WXC, X) + np.dot(self.WHC, np.multiply(r, hPrev)) + self.bC
        c = np.tanh(cbar)

        # Hidden State
        h = np.multiply(c, z) + np.multiply(hPrev, 1 - z)
        # h = np.multiply(z, hPrev) + np.multiply((1 - z), c)


        # Output
        o = softmax(np.dot(self.WY, h) + self.bY, temperature)

        return z, zbar, r, rbar, c, cbar, h, o

    def step(self):
        # Hidden State
        self.h = {}
        self.h[-1] = np.zeros((self.hiddenLayers, 1))

        # Update Gates
        z = {}
        zbars = {}

        # Reset Gates
        r = {}
        rbars = {}

        # Candidates
        c = {}
        cbars = {}

        # Inputs
        x = {}

        # Outputs
        o = {}

        # Target Indexes
        targets = {}

        # Timesteps to Unroll
        totalLen = len(self.inputs)
        if self.cursor + self.sequenceLength > totalLen:
            self.cursor = 0

        # Total Loss
        loss = 0

        for i in xrange(self.sequenceLength):
            # Get inputs and outputs
            X = self.inputs[self.cursor + i]
            y = self.outputs[self.cursor + i]

            # Move inputs forward through network
            z[i], zbars[i], r[i], rbars[i], c[i], cbars[i], self.h[i], o[i] = self.forward(X, self.h[i - 1])

            # Calculate loss
            target = np.argmax(y)
            loss += -np.log(o[i][target, 0])

            x[i] = X
            targets[i] = target

        # Back Propagation
        dXZ = np.zeros_like(self.WXZ)
        dXR = np.zeros_like(self.WXR)
        dXC = np.zeros_like(self.WXC)

        dHZ = np.zeros_like(self.WHZ)
        dHR = np.zeros_like(self.WHR)
        dHC = np.zeros_like(self.WHC)

        dbZ = np.zeros_like(self.bZ)
        dbR = np.zeros_like(self.bR)
        dbC = np.zeros_like(self.bC)
        dbY = np.zeros_like(self.bY)

        dY = np.zeros_like(self.WY)

        dhnext = np.zeros_like(self.h[0])
        dzbarnext = np.zeros_like(zbars[0])
        drbarnext = np.zeros_like(rbars[0])
        dcbarnext = np.zeros_like(cbars[0])

        z[self.sequenceLength] = np.zeros_like(z[0])
        r[self.sequenceLength] = np.zeros_like(r[0])

        for i in reversed(xrange(self.sequenceLength)):
            # Back Propagate Through Y
            dSY = np.copy(o[i])
            dSY[targets[i]] -= 1
            dY += np.dot(dSY, self.h[i].T)
            dbY += dSY

            # Back Propagate Through H and X
            dha = np.multiply(dhnext, 1 - z[i + 1]) # Through Update Gate
            dhb = np.dot(self.WHR.T, drbarnext) # Weights into rbar
            dhc = np.dot(self.WHZ.T, dzbarnext) # Weights into zbar
            dhd = np.multiply(r[i + 1], np.dot(self.WHC.T, dcbarnext)) # Weights into cbar
            dhe = np.dot(self.WY.T, dSY) # Weights at output

            dh = dha + dhb + dhc + dhd + dhe

            dcbar = np.multiply(np.multiply(dh, z[i]) , 1 - np.square(c[i]))
            drbar = np.multiply(np.multiply(self.h[i - 1], np.dot(self.WHC.T, dcbar)), np.multiply(r[i] , (1 - r[i])))
            dzbar = np.multiply(np.multiply(dh, (c[i] - self.h[i - 1])), np.multiply(z[i], (1 - z[i])))

            dXZ += np.dot(dzbar, x[i].T)
            dXR += np.dot(drbar, x[i].T)
            dXC += np.dot(dcbar, x[i].T)

            dHZ += np.dot(dzbar, self.h[i - 1].T)
            dHR += np.dot(drbar, self.h[i - 1].T)
            dHC += np.dot(dcbar, np.multiply(r[i], self.h[i - 1]).T)

            dbZ += dzbar
            dbR += drbar
            dbC += dcbar

            dhnext = dh
            drbarnext = drbar
            dzbarnext = dzbar
            dcbarnext = dcbar


        # Parameter Update (Adam)
        for param, delta, m, v in zip([self.WXZ,   self.WXR,  self.WXC,  self.WHZ,  self.WHR,  self.WHC,  self.WY,  self.bZ,   self.bR,  self.bC],
                                      [dXZ,        dXR,       dXC,       dHZ,       dHR,       dHC,       dY,       dbZ,       dbR,      dbC],
                                      [self.dXZM,  self.dXRM, self.dXCM, self.dHZM, self.dHRM, self.dHCM, self.dYM, self.dbZM, self.dbRM, self.dbCM],
                                      [self.dXZV,  self.dXRV, self.dXCV, self.dHZV, self.dHRV, self.dHCV, self.dYV, self.dbZV, self.dbRV, self.dbCV]):
            m = 0.9 * m + 0.1 * delta
            v = 0.99 * v + 0.01 * (delta ** 2)
            param += -self.learningRate * m / (np.sqrt(v) + 1e-8)

        # Update cursor
        self.cursor += self.sequenceLength

        return loss


    def sample(self, num=100, temperature=1.0, start=False):
        # Output
        output = ""

        # Sample hidden state
        h = {}
        h[-1] = np.zeros((self.hiddenLayers, 1))

        # Sample Update Gate
        z = {}
        zbar = {}

        # Sample Reset Gate
        r = {}
        rbar = {}

        # Sample Candidate Gate
        c = {}
        cbar = {}

        # Make inputs from seed
        if start == False:
            lastCursor = self.cursor - self.sequenceLength
            seedIdx = lastCursor if lastCursor >= 0 else 0
            seed = self.data[seedIdx]
        else:
            seedIdx = self.gramToIndex[start]
            seed = start

        X = np.zeros((self.vocabSize, 1))
        X[self.gramToIndex[seed], 0] = 1

        # Add seed to output
        output += seed

        # Generate sample
        for i in xrange(num - 1):
            # Move through network
            z[i], zbar[i], r[i], rbar[i], c[i], cbar[i], h[i], prediction = self.forward(X, h[i - 1], temperature)

            # Pick ngram using probabilities
            idx = np.random.choice(range(self.vocabSize), p=prediction.ravel())

            # Add to output
            output += self.delimiter + self.indexToGram[idx]

            # Update input to feed back in
            X = np.zeros((self.vocabSize, 1))
            X[idx, 0] = 1


        return output

    def run(self, iterations=1000, size=100, temperatures=[1.0], sampleFile=False, printSample=5, seed=False):
        if sampleFile != False:
            sampleFile = open(sampleFile, 'w')
        for i in xrange(iterations):
            loss = bot.step()
            if i % printSample == 0:
                for temperature in temperatures:
                    print '======= Temperature: ' + str(temperature) + ' ======='
                    sample = bot.sample(size, temperature, seed)
                    print sample
                    if(sampleFile != False):
                        sampleFile.write(sample + '\n\n\n')

                print '\n'
                print '======= Iteration ' + str(i + 1) + ' ======='
                print '======= Samples Seen: ' + str(self.cursor) + ' ======='
                print '======= Loss: ' + str(loss) + ' ======='

        if sampleFile != False:
            sampleFile.close()

    def save(self, small=True):
        savedObj = {item:value for item, value in self.__dict__.iteritems()}

        if small == True:
            for param in ["data", "uniqueData", "indexToGram", "gramToIndex", "inputs", "outputs"]:
                del savedObj[param]

        pickle.dump(savedObj, open("data/MODEL", "w+"))

    def load(self, dump):
        newSelf = pickle.load(dump)
        for item, value in newSelf.iteritems():
            setattr(self, item, value)

data = open('data/data.txt').read().lower()
bot = TextRNN()
bot.train(data, 1, '')
bot.load(open("data/MODEL"));
bot.run(size=50, temperatures=[0.5, 1.0], iterations=5000)
bot.save(True)
# print bot.sample(300000, temperature=0.5, start='\n')
