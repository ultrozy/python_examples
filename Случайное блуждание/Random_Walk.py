import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation

ANIMATION = True    # Анимация или Рисунок
STD = 1.0         # Стандартное отклонение на каждом шаге

if ANIMATION:
    # При True - сохраняет цвет каждого шага
    # При False - цветовой след:
    #   чем ближе точка к текущему положению - тем ближе к красному по радуге
    #   чем дальше точка от текущего положения - тем она ближе к фиолетовому по радуге
    PRESERVE_COLORS = False
    N = 100         # количество точек на экране
    SAME_COLOR = 1  # количество точек с одинаковым цветом
    RESERVE = 100   # количество заранее вычисленных точек, не может быть меньше N
    
    # Параметры matplotlib
    LINEWIDTH = 2   # Ширина линии
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.axhline(y=0, color='k')
    ax.axvline(x=0, color='k')
    ax.axis("equal")    # Оси в равном масштабе (не сужены и не расширены)

    # Корректировка параметров в случае некорректных исходных значений
    N = N + SAME_COLOR - (N-1) % SAME_COLOR - 1
    RESERVE = max(RESERVE, N+100)
    RESERVE = RESERVE + SAME_COLOR - (RESERVE-1) % SAME_COLOR - 1
    # Формирование цветового массива
    # При разных значениях параметра PRESERVE_COLORS цветовой массив различен
    NUM_COLORS = N // SAME_COLOR
    if PRESERVE_COLORS:
        COLOR_SET = [(1.0, 0.0, 0.0) for j in range(NUM_COLORS)]
        for j in range(1, NUM_COLORS):
            _color = (j * 6.0) / NUM_COLORS
            if _color < 1.0:
                _color = (1.0, _color, 0.0)
            elif _color < 2.0:
                _color = (2.0-_color, 1.0, 0.0)
            elif _color < 3.0:
                _color = (0.0, 1.0, _color-2.0)
            elif _color < 4.0:
                _color = (0.0, 4.0-_color, 1.0)
            elif _color < 5.0:
                _color = (_color-4.0, 0.0, 1.0)
            else:
                _color = (1.0, 0.0, 6.0-_color)
            COLOR_SET[j] = _color
    else:
        COLOR_SET = [(1.0, 0.0, 1.0) for j in range(NUM_COLORS)]
        COLOR_SET[-1] = (1.0, 0.0, 0.0)
        for j in range(1, NUM_COLORS-1):
            _color = (j * 5.0) / NUM_COLORS
            if _color < 1.0:
                _color = (1.0-_color, 0.0, 1.0)
            elif _color < 2.0:
                _color = (0.0, _color-1.0, 1.0)
            elif _color < 3.0:
                _color = (0.0, 1.0, 3.0-_color)
            elif _color < 4.0:
                _color = (_color-3.0, 1.0, 0.0)
            else:
                _color = (1.0, 5.0-_color, 0.0)
            COLOR_SET[j] = _color
    
    X = np.zeros(RESERVE, dtype=np.float64)
    Y = np.zeros(RESERVE, dtype=np.float64)
    X[N:] = np.random.randn(RESERVE-N) * STD
    Y[N:] = np.random.randn(RESERVE-N) * STD
    X = np.cumsum(X)
    Y = np.cumsum(Y)
    shift = 0
    def animate(i):
        global shift
        ax.clear()
        if PRESERVE_COLORS:
            for j in range(0, N-SAME_COLOR, SAME_COLOR):
                ax.plot(X[i+j-shift: i+j-shift+SAME_COLOR+1],
                        Y[i+j-shift: i+j-shift+SAME_COLOR+1],
                        color=COLOR_SET[(i+j) % NUM_COLORS],
                        linewidth=LINEWIDTH)
            ax.plot(X[i+N-SAME_COLOR-shift: i+N-shift],
                    Y[i+N-SAME_COLOR-shift: i+N-shift],
                    color=COLOR_SET[(i+N-SAME_COLOR) % NUM_COLORS],
                    linewidth=LINEWIDTH)
        else:
            for j in range(0, N-SAME_COLOR, SAME_COLOR):
                ax.plot(X[i+j-shift: i+j-shift+SAME_COLOR+1],
                        Y[i+j-shift: i+j-shift+SAME_COLOR+1],
                        color=COLOR_SET[j % NUM_COLORS],
                        linewidth=LINEWIDTH)
            ax.plot(X[i+N-SAME_COLOR-shift: i+N-shift],
                    Y[i+N-SAME_COLOR-shift: i+N-shift],
                    color=COLOR_SET[-1],
                    linewidth=LINEWIDTH)
        ax.scatter(X[i+N-shift-1], Y[i+N-shift-1], c="k", s=70)
        if i+N-shift == RESERVE:
            shift += RESERVE - N
            X[:N] = X[RESERVE-N:]
            Y[:N] = Y[RESERVE-N:]
            X[N:] = np.random.randn(RESERVE-N).cumsum() * STD + X[N-1]
            Y[N:] = np.random.randn(RESERVE-N).cumsum() * STD + Y[N-1]
    anim = matplotlib.animation.FuncAnimation(fig, animate, interval=10)
    plt.show()
    
    
    
    
    
else:
    N = 10000
    SAME_COLOR = 10

    plt.rcParams['lines.linewidth'] = 0.5
    plt.axhline(y=0, color='k')
    plt.axvline(x=0, color='k')
    plt.axis("equal")

    colors=list(zip(np.full((N//5), 1.0), np.linspace(0.0, 1.0, N//5), np.full((N//5), 0.0)))
    colors.extend(list(zip(np.linspace(1.0, 0.0, N//5), np.full((N//5), 1.0), np.full((N//5), 0.0))))
    colors.extend(list(zip(np.full((N//5), 0.0), np.full((N//5), 1.0), np.linspace(0.0, 1.0, N//5))))
    colors.extend(list(zip(np.full((N//5), 0.0), np.linspace(1.0, 0.0, N//5), np.full((N//5), 1.0))))
    colors.extend(list(zip(np.linspace(0.0, 1.0, N//5), np.full((N//5), 0.0), np.full((N//5), 1.0))))

    X = np.random.randn(N) * STD
    Y = np.random.randn(N) * STD
    X[0] = Y[0] = 0
    X = np.cumsum(X)
    Y = np.cumsum(Y)

    for i in range(0, N, SAME_COLOR):
        plt.plot(X[i:i+SAME_COLOR+1], Y[i:i+SAME_COLOR+1], color=colors[i])
    if X[0] < X[-1]:
        if Y[0] < Y[-1]:
            xystart = (0.02,0.02)
            xyend = (0.93,0.95)
        else:
            xystart = (0.02, 0.95)
            xyend = (0.93, 0.02)
    else:
        if Y[0] < Y[-1]:
            xystart = (0.92, 0.02)
            xyend = (0.02, 0.95)
        else:
            xystart = (0.92, 0.95)
            xyend = (0.02, 0.02)
    plt.annotate("start", xy=(X[0], Y[0]), textcoords="axes fraction", xytext=xystart, arrowprops=dict(facecolor='k', width=1, headwidth=5))
    plt.annotate("end", xy=(X[-1], Y[-1]), textcoords="axes fraction", xytext=xyend, arrowprops=dict(facecolor='k', width=1, headwidth=5))
    plt.show()