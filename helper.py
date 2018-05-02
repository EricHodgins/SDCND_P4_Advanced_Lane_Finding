def plot_images(images, rows, cols, cmap=None):
    fig = plt.figure()
    for i, image in enumerate(images,1):
        ax = fig.add_subplot(rows, cols, i)
        ax.imshow(image.squeeze(), cmap=cmap)