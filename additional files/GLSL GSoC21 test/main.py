from shader import *
from model import *
from math import *
from PIL import Image


print(OpenGL.__version__)

width = 1280
height = 720



def main():
    if not glfw.init():
        return
    window = glfw.create_window(width, height, "Shader Test", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.swap_interval(1)
    glfw.window_hint(glfw.SAMPLES, 40)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_MULTISAMPLE)

    viewPos = glm.vec3(-10, 0, 0)
    perspective = glm.perspective(45, width / height, 0.1, 10000)

    fire = Shader("shaders/fire.vert", "shaders/fire.frag")
    manModel = Model("man.json")
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    noiseWidth = 512
    SHAPE = (noiseWidth, noiseWidth)

    noise = np.random.normal(255. / 2, 255. / 20, SHAPE)
    image = Image.fromarray(noise)
    image = image.convert('RGB')
    img_data = np.array(list(image.getdata()), np.uint8)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, noiseWidth, noiseWidth, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)

    while not glfw.window_should_close(window):

        camX = sin(glfw.get_time()) * 7
        camZ = cos(glfw.get_time()) * 7
        lightPos = glm.vec3(camX, 5, camZ)
        view = glm.lookAt(glm.vec3(0, 5, 10), glm.vec3(0, 5, 10) + glm.vec3(0, 0, -1), glm.vec3(0, 1, 0))

        glViewport(0, 0, width, height)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0, 0, 0, 1)

        fire.use()
        fire.setFloat("Time", glfw.get_time())
        fire.setMat4('viewProject', perspective * view)
        fire.setVec3('viewPos', viewPos)
        fire.setVec3('lightPos', lightPos)
        fire.setVec3('lightPos', lightPos)
        scale = glm.scale(manModel.model, glm.vec3(0.3, 0.3, 0.3))
        fire.setMat4('model', scale)
        manModel.draw(fire)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()
