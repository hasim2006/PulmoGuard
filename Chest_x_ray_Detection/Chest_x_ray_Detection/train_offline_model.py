import os
import glob
import numpy as np
from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "..", "chest_xray")
MODEL_SAVE_PATH = os.path.join(BASE_DIR, "offline_model.npz")

IMG_SIZE = 48

def load_img_features(path):
    try:
        with Image.open(path) as img:
            img = img.convert('L').resize((IMG_SIZE, IMG_SIZE), Image.Resampling.BILINEAR)
            arr = np.asarray(img, dtype=np.float32) / 255.0
            # Center contrast normalization
            mean = np.mean(arr)
            std = np.std(arr) + 1e-5
            arr = (arr - mean) / std
            return arr.flatten()
    except Exception as e:
        return None

def main():
    print("Gathering training images...")
    norm_paths = glob.glob(os.path.join(DATA_DIR, "train", "NORMAL", "*.jpeg"))
    pneu_paths = glob.glob(os.path.join(DATA_DIR, "train", "PNEUMONIA", "*.jpeg"))
    
    # Balanced subset for quick, high-performance training
    n_samples = min(len(norm_paths), 1000)
    print(f"Using {n_samples} Normal and {n_samples} Pneumonia images...")
    
    X_list = []
    y_list = []
    
    for p in norm_paths[:n_samples]:
        feat = load_img_features(p)
        if feat is not None:
            X_list.append(feat)
            y_list.append([1.0, 0.0]) # [Normal, Pneumonia]
            
    for p in pneu_paths[:n_samples]:
        feat = load_img_features(p)
        if feat is not None:
            X_list.append(feat)
            y_list.append([0.0, 1.0]) # [Normal, Pneumonia]
            
    X = np.array(X_list, dtype=np.float32)
    y = np.array(y_list, dtype=np.float32)
    
    # Shuffle
    indices = np.arange(len(X))
    np.random.seed(42)
    np.random.shuffle(indices)
    X = X[indices]
    y = y[indices]
    
    input_dim = IMG_SIZE * IMG_SIZE
    hidden_dim = 64
    output_dim = 2
    
    # Xavier initialization
    W1 = np.random.randn(input_dim, hidden_dim).astype(np.float32) * np.sqrt(2.0 / input_dim)
    b1 = np.zeros(hidden_dim, dtype=np.float32)
    W2 = np.random.randn(hidden_dim, output_dim).astype(np.float32) * np.sqrt(2.0 / hidden_dim)
    b2 = np.zeros(output_dim, dtype=np.float32)
    
    lr = 0.01
    batch_size = 32
    epochs = 40
    
    print("Training offline neural network...")
    for epoch in range(epochs):
        perm = np.random.permutation(len(X))
        for i in range(0, len(X), batch_size):
            xb = X[perm[i:i+batch_size]]
            yb = y[perm[i:i+batch_size]]
            
            # Forward pass (ReLU + Softmax)
            z1 = np.dot(xb, W1) + b1
            a1 = np.maximum(0, z1)
            z2 = np.dot(a1, W2) + b2
            exp_z2 = np.exp(z2 - np.max(z2, axis=1, keepdims=True))
            probs = exp_z2 / np.sum(exp_z2, axis=1, keepdims=True)
            
            # Backpropagation
            dz2 = (probs - yb) / len(xb)
            dW2 = np.dot(a1.T, dz2)
            db2 = np.sum(dz2, axis=0)
            
            da1 = np.dot(dz2, W2.T)
            dz1 = da1 * (z1 > 0)
            dW1 = np.dot(xb.T, dz1)
            db1 = np.sum(dz1, axis=0)
            
            # Gradient update
            W1 -= lr * dW1
            b1 -= lr * db1
            W2 -= lr * dW2
            b2 -= lr * db2
            
        if (epoch + 1) % 10 == 0:
            preds = np.argmax(probs, axis=1)
            acc = np.mean(preds == np.argmax(yb, axis=1))
            print(f"Epoch {epoch+1}/{epochs} - Batch Accuracy: {acc*100:.1f}%")
            
    # Evaluate on test set
    test_norm = glob.glob(os.path.join(DATA_DIR, "test", "NORMAL", "*.jpeg"))
    test_pneu = glob.glob(os.path.join(DATA_DIR, "test", "PNEUMONIA", "*.jpeg"))
    
    test_X = []
    test_y = []
    for p in test_norm:
        f = load_img_features(p)
        if f is not None:
            test_X.append(f)
            test_y.append(0)
    for p in test_pneu:
        f = load_img_features(p)
        if f is not None:
            test_X.append(f)
            test_y.append(1)
            
    test_X = np.array(test_X)
    test_y = np.array(test_y)
    
    z1 = np.maximum(0, np.dot(test_X, W1) + b1)
    z2 = np.dot(z1, W2) + b2
    exp_z = np.exp(z2 - np.max(z2, axis=1, keepdims=True))
    test_probs = exp_z / np.sum(exp_z, axis=1, keepdims=True)
    test_preds = np.argmax(test_probs, axis=1)
    test_acc = np.mean(test_preds == test_y)
    print(f"Test Set Accuracy: {test_acc*100:.2f}% on {len(test_y)} unseen test X-rays!")
    
    # Save weights
    np.savez_compressed(MODEL_SAVE_PATH, W1=W1, b1=b1, W2=W2, b2=b2, img_size=IMG_SIZE)
    print(f"Model successfully saved to: {MODEL_SAVE_PATH}")

if __name__ == "__main__":
    main()
