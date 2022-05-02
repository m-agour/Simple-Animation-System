#version 450

in vec4 vertexColor;
out vec4 FragColor;
layout (location=0) uniform float time;
layout (location=1) uniform vec4 color;

void main(){
    FragColor = vec4(1, 1, 1, 1);
//    FragColor = vec4(sin(time), cos(time), 0, 1);
}