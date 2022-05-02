#version 450

in vec4 aPos;
in vec3 aNorm;
out vec4 vertexColor;

void main(){
    gl_Position = aPos;
    vertexColor = vec4(aPos.xyz, 1);
}