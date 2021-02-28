import cv2
from numpy import ndarray
from collections import deque


def hsv(b, g, r):
    bgr_min, bgr_max = min(b, g, r), max(b, g, r)

    h, s, v = 0., 0, 0

    v = bgr_max
    if bgr_max == 0:
        return h, s, v

    gap = bgr_max - bgr_min
    s = (255 * gap) // bgr_max
    if gap == 0:
        return h, s, v

    if bgr_max == r:
        h = 43 * (g / gap - b / gap)
    elif bgr_max == g:
        h = 85 + 43 * (b / gap - r / gap)
    else:
        h = 171 + 43 * (r / gap - g / gap)

    if h > 255:
        h = 255
    elif h < 0:
        h = int(h + 255)
    else:
        h = int(h)
    return h, s, v


def bgr2hsv(src):
    height, width, n_channels = src.shape
    dst = ndarray(
        shape=src.shape,
        dtype=src.dtype
    )

    for y in range(height):
        for x in range(width):
            dst[y][x][0], dst[y][x][1], dst[y][x][2] = hsv(src[y][x][0], src[y][x][1], src[y][x][2])
            # bgr_min, bgr_max = src[y][x][0], src[y][x][0]
            # for i in range(1, 3):
            #     if bgr_max < src[y][x][i]:
            #         bgr_max = src[y][x][i]
            #     elif bgr_min > src[y][x][i]:
            #         bgr_min = src[y][x][i]
            #
            # dst[y][x][2] = bgr_max
            # if bgr_max == 0:
            #     dst[y][x][1] = dst[y][x][0] = 0
            #     continue
            #
            # gap = bgr_max - bgr_min
            # dst[y][x][1] = (255 * gap) // bgr_max
            # if gap == 0:
            #     dst[y][x][1] = 0
            #     continue
            #
            # h = 0.
            # if bgr_max == src[y][x][2]:
            #     h = 43 * (src[y][x][1] / gap - src[y][x][0] / gap)
            # elif bgr_max == src[y][x][1]:
            #     h = 85 + 43 * (src[y][x][0] / gap - src[y][x][2] / gap)
            # else:
            #     h = 171 + 43 * (src[y][x][2] / gap - src[y][x][1] / gap)
            #
            # if h > 255:
            #     dst[y][x][0] = 255
            # elif h < 0:
            #     dst[y][x][0] = int(h + 255)
            # else:
            #     dst[y][x][0] = int(h)
    return dst


def red_detect(src):
    height, width, n_channels = src.shape
    dst = ndarray(
        shape=src.shape,
        dtype=src.dtype
    )

    for y in range(height):
        for x in range(width):
            if (src[y][x][0] >= 250 or src[y][x][0] <= 5) and src[y][x][1] > 160 and src[y][x][2] > 30:
                dst[y][x][2] = dst[y][x][1] = dst[y][x][0] = 255
            else:
                dst[y][x][2] = dst[y][x][1] = dst[y][x][0] = 0

    return dst


def dilate(src):
    height, width, n_channels = src.shape
    dst = ndarray(
        shape=src.shape,
        dtype=src.dtype
    )

    y, x = 0, 0
    while x < width - 1:
        dst[y][x][2] = dst[y][x][1] = dst[y][x][0] = src[y][x][0]
        x += 1
    while y < height - 1:
        dst[y][x][2] = dst[y][x][1] = dst[y][x][0] = src[y][x][0]
        y += 1
    while x > 0:
        dst[y][x][2] = dst[y][x][1] = dst[y][x][0] = src[y][x][0]
        x -= 1
    while y > 0:
        dst[y][x][2] = dst[y][x][1] = dst[y][x][0] = src[y][x][0]
        y -= 1

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            dst[y][x][0] = max(max(src[i][j][0] for j in range(x - 1, x + 2)) for i in range(y - 1, y + 2))
            dst[y][x][2] = dst[y][x][1] = dst[y][x][0]
    return dst


dy = [0, 1, 1, 1, 0, -1, -1, -1]
dx = [1, 1, 0, -1, -1, -1, 0, 1]


def erode(src):
    height, width, n_channels = src.shape
    dst = ndarray(
        shape=src.shape,
        dtype=src.dtype
    )

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            dst[y][x][0] = dst[y][x][1] = dst[y][x][2] = 0
            if src[y][x][0]:
                for d in range(8):
                    if not src[y + dy[d]][x + dx[d]][0]:
                        break
                else:
                    dst[y][x][0] = dst[y][x][1] = dst[y][x][2] = 255

    return dst


def labeling(src):
    height, width, n_channels = src.shape
    dst = ndarray(
        shape=src.shape,
        dtype=src.dtype
    )

    vst = [[False] * width for _ in range(height)]
    nl = 0
    labels = [0]
    for y in range(height):
        for x in range(width):
            if not vst[y][x]:
                vst[y][x] = True
                if src[y][x][0]:
                    queue = deque([[y, x]])
                    stack = deque([[y, x]])
                    cnt = 1
                    while queue:
                        vy, vx = queue.popleft()
                        for k in range(8):
                            uy, ux = vy + dy[k], vx + dx[k]
                            if 0 <= uy < height and 0 <= ux < width:
                                if not vst[uy][ux] and src[uy][ux][0]:
                                    vst[uy][ux] = True
                                    queue.append([uy, ux])
                                    stack.append([uy, ux])
                                    cnt += 1
                    l = 0
                    if cnt > 100:
                        nl += 1
                        l = nl
                        labels.append(cnt)
                    while stack:
                        vy, vx = stack.pop()
                        dst[vy][vx][2] = dst[vy][vx][1] = dst[vy][vx][0] = l
                else:
                    dst[y][x][2] = dst[y][x][1] = dst[y][x][0] = 0
    return dst, labels


def histogram(hsv, bin, labels):
    height, width, n_channels = bin.shape
    hist = [[[0] * 256 for _ in range(3)] for _ in range(len(labels))]

    for y in range(height):
        for x in range(width):
            i = bin[y][x][0]
            if i:
                hist[i][0][hsv[y][x][0]] += 1
                hist[i][1][hsv[y][x][1]] += 1
                hist[i][2][hsv[y][x][2]] += 1

    for i in range(1, len(labels)):
        for j in range(256):
            hist[i][0][j] /= labels[i]
            hist[i][1][j] /= labels[i]
            hist[i][2][j] /= labels[i]

    return hist


def object_detect(src, bin, cam_hist, sam_hist):
    height, width, n_channels = bin.shape
    dst = ndarray(
        shape=bin.shape,
        dtype=bin.dtype
    )

    Ki = [0] * len(cam_hist)
    for i in range(1, len(cam_hist)):
        for j in range(256):
            if sam_hist[1][0][j] + cam_hist[i][0][j]:
                Ki[i] += (sam_hist[1][0][j] - cam_hist[i][0][j]) ** 2 / (sam_hist[1][0][j] + cam_hist[i][0][j])
            if sam_hist[1][1][j] + cam_hist[i][1][j]:
                Ki[i] += (sam_hist[1][1][j] - cam_hist[i][1][j]) ** 2 / (sam_hist[1][1][j] + cam_hist[i][1][j])
            if sam_hist[1][2][j] + cam_hist[i][2][j]:
                Ki[i] += (sam_hist[1][2][j] - cam_hist[i][2][j]) ** 2 / (sam_hist[1][2][j] + cam_hist[i][2][j])

    minL = 1
    for i in range(2, len(cam_hist)):
        if Ki[minL] > Ki[i]:
            minL = i

    for y in range(height):
        for x in range(width):
            if bin[y][x][0] == minL:
                # dst[y][x][2] = dst[y][x][1] = dst[y][x][0] = 255
                dst[y][x][0] = src[y][x][0]
                dst[y][x][1] = src[y][x][1]
                dst[y][x][2] = src[y][x][2]
            else:
                dst[y][x][2] = dst[y][x][1] = dst[y][x][0] = 0

    return dst


def hsv2black(src):
    height, width, n_channels = src.shape
    dst = ndarray(
        shape=src.shape,
        dtype=src.dtype
    )

    for y in range(height):
        for x in range(width):
            if src[y][x][2] < 70:
                dst[y][x][0] = dst[y][x][1] = dst[y][x][2] = 255
            else:
                dst[y][x][0] = dst[y][x][1] = dst[y][x][2] = 0

    return dst


def prewitt(src):
    height, width, n_channels = src.shape
    dst = ndarray(
        shape=src.shape,
        dtype=src.dtype
    )

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            h1 = sum(src[y + 1][x + i][0] for i in range(-1, 2)) - sum(src[y - 1][x - i][0] for i in range(-1, 2))
            h2 = sum(src[y + i][x + 1][0] for i in range(-1, 2)) - sum(src[y - i][x - 1][0] for i in range(-1, 2))
            hVal = h1 * h1 + h2 * h2
            if hVal > 10000:
                dst[y][x][0] = dst[y][x][1] = dst[y][x][2] = 255
            else:
                dst[y][x][0] = dst[y][x][1] = dst[y][x][2] = 0

    return dst


COS3 = [
    1.000000, 0.998630, 0.994522, 0.987688, 0.978148,
    0.965926, 0.951057, 0.933580, 0.913545, 0.891007,
    0.866025, 0.838671, 0.809017, 0.777146, 0.743145,
    0.707107, 0.669131, 0.629321, 0.587785, 0.544639,
    0.500000, 0.453991, 0.406737, 0.358368, 0.309017,
    0.258819, 0.207912, 0.156435, 0.104529, 0.052336,
    0.000000
]
SIN3 = [
    0.000000, 0.052336, 0.104528, 0.156434, 0.207912,
    0.258819, 0.309017, 0.358368, 0.406737, 0.453990,
    0.500000, 0.544639, 0.587785, 0.629320, 0.669131,
    0.707107, 0.743145, 0.777146, 0.809017, 0.838670,
    0.866025, 0.891006, 0.913545, 0.933580, 0.951056,
    0.965926, 0.978148, 0.987688, 0.994522, 0.998630,
    1.000000
]


def hough_line(src):
    height, width, n_channels = src.shape
    dst = ndarray(
        shape=src.shape,
        dtype=src.dtype
    )
    for y in range(height):
        for x in range(width):
            dst[y][x][0] = dst[y][x][1] = dst[y][x][2] = 0

    THRES = 120
    DIAGONAL = 500
    count = [[0] * 60 for _ in range(DIAGONAL << 1)]

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            if src[y][x][0]:
                for t in range(31):
                    r = int(COS3[t] * x + SIN3[t] * y)
                    if -width < r < width:
                        count[r + width][t] += 1
                for t in range(31, 60):
                    r = int(-COS3[60 - t] * x + SIN3[60 - t] * y)
                    if -width < r < width:
                        count[r + width][t] += 1

    for t in range(0, 60):
        for r in range(-width, width):
            if count[r + width][t] > THRES:
                if t <= 30:
                    for x in range(width):
                        y = int((r - COS3[t] * x) / SIN3[t])
                        if 0 <= y < height:
                            dst[y][x][0] = dst[y][x][1] = dst[y][x][2] = 255
                else:
                    for x in range(width):
                        y = int((r + COS3[60 - t] * x) / SIN3[60 - t])
                        if 0 <= y < height:
                            dst[y][x][0] = dst[y][x][1] = dst[y][x][2] = 255
    return dst


def main():
    # # object detect
    # bgr_img = cv2.imread('images/bgr_img.jpg', 1)
    # hsv_img = bgr2hsv(bgr_img)
    # red_img = red_detect(hsv_img)
    # dilated_img = dilate(red_img)
    # labeled_img, labels = labeling(dilated_img)
    # sam_hist = histogram(hsv_img, labeled_img, labels)
    #
    # problem_img = cv2.imread('images/problem_img.jpg', 1)
    # hsv_img = bgr2hsv(problem_img)
    # red_img = red_detect(hsv_img)
    # dilated_img = dilate(red_img)
    # labeled_img, labels = labeling(dilated_img)
    # cam_hist = histogram(hsv_img, labeled_img, labels)
    # detected_img = object_detect(problem_img, labeled_img, cam_hist, sam_hist)
    #
    # cv2.imshow('bgr_img', bgr_img)
    # cv2.imshow('problem_img', problem_img)
    # cv2.imshow('detected_img', detected_img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # cv2.imwrite('images/dilated_img.jpg', dilated_img)

    # line detect
    bgr_img = cv2.imread('images/line.png', 1)
    hsv_img = bgr2hsv(bgr_img)
    black_img = hsv2black(hsv_img)
    eroded_img = erode(black_img)
    prewitted_img = prewitt(eroded_img)
    lined_img = hough_line(prewitted_img)

    cv2.imshow('bgr_img', bgr_img)
    cv2.imshow('prewitted_img', prewitted_img)
    cv2.imshow('lined_img', lined_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    # cv2.imwrite('images/dilated_img.jpg', dilated_img)


if __name__ == '__main__':
    main()
