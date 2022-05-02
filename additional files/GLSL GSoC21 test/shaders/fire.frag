#version 440

layout (location=0) uniform float Time;
layout (binding=0) uniform sampler2D noiseTex;
out vec4 fragColor;
in vec3 fragPos;
in vec3 normal;




struct Material
{
    vec3 ambient;
    vec3 diffuse;
    vec3 specular;
    float shininess;
};

struct PointLight
{
    vec3 position;
    vec3 diffuse;
    vec3 ambient;
    vec3 specular;
    float constant;
    float linear;
    float quadratic;
};


uniform vec3 viewPos;
uniform float farPlane;
uniform vec3 lightPos;
uniform samplerCube depthMap;
uniform PointLight light;
Material material;

vec3 calcPointLight(PointLight light, vec3 normal, vec3 viewDir)
{
    vec3 fragToLightDir = light.position - fragPos;
    float distances = length(fragToLightDir);
    fragToLightDir = normalize(fragToLightDir);
    float wek = 1.0 / (light.constant + light.linear * distances + light.quadratic * pow(distances, 2));

    float diff = max(dot(fragToLightDir, normal), 0.0);
    vec3 halfwayDir = normalize(fragToLightDir + viewDir);
    float specAngle = max(dot(halfwayDir, normal), 0.0);
    float spec = pow(specAngle, material.shininess);

    vec3 ambient = light.ambient * material.ambient * wek;
    vec3 diffuse = light.diffuse * diff * wek;
    vec3 specular = light.specular * spec * wek;
    return (ambient *2 + diffuse + specular) * (material.diffuse + material.specular);
}


#define time Time*0.01

float hash21(in vec2 n){ return fract(sin(dot(n, vec2(12.9898, 4.1414))) * 43758.5453); }
mat2 makem2(in float theta){float c = cos(theta);float s = sin(theta);return mat2(c,-s,s,c);}
float noise( in vec2 x ){return texture(noiseTex, x*.01).x;}

vec2 gradn(vec2 p)
{
	float ep = .09;
	float gx = noise(vec2(p.x+ep,p.y))-noise(vec2(p.x-ep,p.y));
	float gy = noise(vec2(p.x,p.y+ep))-noise(vec2(p.x,p.y-ep));
	return vec2(gx,gy);
}

float f(in vec2 p)
{
	float z=2.;
	float rz = 0.;
	vec2 bp = p;
	for (float i= 1.;i < 7.;i++ )
	{
		p += time*.6;
		bp += time*10.9;
		vec2 gr = gradn(-i*p*.34+time*1.);
		gr*=makem2(time*6.-(0.05*p.x+0.03*p.y)*40.);
		p += gr*.5;
		rz+= (sin(noise(p)*7.)*0.5+0.5)/z;
		p = mix(bp,p,.77);
		z *= 3.4;
		p *= 6.;
		bp *= 1.9;
	}
	return rz;
}

void main()
{
	vec2 resolution = vec2(-5, -5);
	vec3 p = fragPos.xyz / resolution.xyx-0.5;
	p.xy *= resolution.x/resolution.y;
	p*= 3.0;
	float rz = f(p.xy);
	vec3 col = vec3(.2,0.07,0.01)/rz;
	col=pow(col,vec3(1.4));
	PointLight light;
    light.position = lightPos;
    light.ambient = vec3(0.27);
    light.diffuse =  vec3(0.7);
    light.specular = vec3(0.55);
    light.constant = 1.0;
    light.linear = 0.01;
    light.quadratic = 0.01;
    material.diffuse = col;
    material.ambient = col;
    material.specular = col;
    material.shininess = 16;

    vec3 norm = normalize(normal);
    vec3 viewDir = normalize(viewPos - fragPos);
    vec3 result = calcPointLight(light, norm, viewDir);
    fragColor = vec4(result, 1.0);
}




