import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

np.random.seed(42)

# 2次元の線形分離可能なデータを生成
# クラス1 (+1): (2, 2) を中心とした正規分布
X1 = np.random.randn(20, 2) + np.array([2, 2])
y1 = np.ones(20)

# クラス2 (-1): (-2, -2) を中心とした正規分布
X2 = np.random.randn(20, 2) + np.array([-2, -2])
y2 = -np.ones(20)

X = np.vstack((X1, X2))
y = np.concatenate((y1, y2))

# バイアス項 (x0 = 1) を特徴量に追加
X_bias = np.hstack((np.ones((X.shape[0], 1)), X))

# 重みの初期化 [w0, w1, w2]
w = np.array([1.0, -0.5, 0.5])
w_initial = w.copy()
w_history = [w_initial.copy()]

print("========================================")
print("初期の重み:", w_initial)

# パーセプトロンの学習アルゴリズム
learning_rate = 0.1
max_epochs = 100
epochs_needed = max_epochs

for epoch in range(max_epochs):
    misclassified = 0
    for i in range(X_bias.shape[0]):
        # 誤分類された場合のみ重みを更新
        if y[i] * np.dot(w, X_bias[i]) <= 0:
            w = w + learning_rate * y[i] * X_bias[i]
            w_history.append(w.copy())
            misclassified += 1
    # 誤分類がなくなったら学習を終了
    if misclassified == 0:
        epochs_needed = epoch + 1
        break

w_history = np.array(w_history)

print(f"学習完了（エポック数: {epochs_needed}）")
print(f"重みの更新回数: {len(w_history) - 1}")
print("最終的な重み:", w)
print("========================================")

# 結果のプロット
fig = plt.figure(figsize=(15, 5))

# ------------------------------
# 分類前のプロット (初期の決定境界)
# ------------------------------
ax1 = fig.add_subplot(1, 3, 1)
ax1.scatter(X1[:, 0], X1[:, 1], color='blue', marker='o', label='Class 1 (+1)')
ax1.scatter(X2[:, 0], X2[:, 1], color='red', marker='x', label='Class 2 (-1)')

x_plot = np.linspace(X[:, 0].min() - 1, X[:, 0].max() + 1, 100)

if w_initial[2] != 0:
    y_plot_initial = -(w_initial[0] + w_initial[1] * x_plot) / w_initial[2]
    ax1.plot(x_plot, y_plot_initial, 'k--', label='Initial Boundary')
else:
    ax1.axvline(x=-w_initial[0]/w_initial[1], color='k', linestyle='--', label='Initial Boundary')

ax1.set_xlim(X[:, 0].min() - 1, X[:, 0].max() + 1)
ax1.set_ylim(X[:, 1].min() - 1, X[:, 1].max() + 1)
ax1.set_title('Initial Decision Boundary')
ax1.set_xlabel('x1')
ax1.set_ylabel('x2')
ax1.legend()
ax1.grid(True)

# ------------------------------
# 分類後のプロット (学習後の決定境界)
# ------------------------------
ax2 = fig.add_subplot(1, 3, 2)
ax2.scatter(X1[:, 0], X1[:, 1], color='blue', marker='o', label='Class 1 (+1)')
ax2.scatter(X2[:, 0], X2[:, 1], color='red', marker='x', label='Class 2 (-1)')

if w[2] != 0:
    y_plot_final = -(w[0] + w[1] * x_plot) / w[2]
    ax2.plot(x_plot, y_plot_final, 'k-', label='Final Boundary')
else:
    ax2.axvline(x=-w[0]/w[1], color='k', linestyle='-', label='Final Boundary')

ax2.set_xlim(X[:, 0].min() - 1, X[:, 0].max() + 1)
ax2.set_ylim(X[:, 1].min() - 1, X[:, 1].max() + 1)
ax2.set_title(f'Final Boundary (Epochs: {epochs_needed})')
ax2.set_xlabel('x1')
ax2.set_ylabel('x2')
ax2.legend()
ax2.grid(True)

# ------------------------------
# 重み空間の遷移 (3Dプロット)
# ------------------------------
ax3 = fig.add_subplot(1, 3, 3, projection='3d')
# 重みの軌跡をプロット
ax3.plot(w_history[:, 0], w_history[:, 1], w_history[:, 2], 
         marker='o', markersize=4, linestyle='-', color='purple', alpha=0.7)

# 開始点と終了点を強調
ax3.scatter(w_history[0, 0], w_history[0, 1], w_history[0, 2], 
            color='red', s=100, label='Start', marker='^')
ax3.scatter(w_history[-1, 0], w_history[-1, 1], w_history[-1, 2], 
            color='green', s=100, label='End', marker='*')

ax3.set_title('Weight Vector Trajectory')
ax3.set_xlabel('w0 (bias)')
ax3.set_ylabel('w1')
ax3.set_zlabel('w2')
ax3.legend()

plt.tight_layout()
plt.savefig('perceptron_boundary_with_history.png', dpi=300)
print("Plot saved as perceptron_boundary_with_history.png")
