<script setup>
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';
import { RGBELoader } from 'three/examples/jsm/loaders/RGBELoader';
import { Water } from 'three/examples/jsm/objects/Water';
import { onMounted, ref, nextTick } from 'vue';
import * as echarts from 'echarts';
import { Chart } from 'chart.js';
import axios from 'axios';
import Papa from 'papaparse'; // 导入 PapaParse

const chartData = ref([]);
const chartCanvas = document.createElement('canvas');
chartCanvas.width = 800;
chartCanvas.height = 400;
const chartContext = chartCanvas.getContext('2d');

const loadCSVData = async () => {
    try {
        const response = await axios.get('/Acceleration_0.csv');
        Papa.parse(response.data, {
            header: true,
            complete: (results) => {
                chartData.value = results.data;
                const chartTexture = createChartTexture();
                // Use chartTexture for sprites or other objects
                console.log(chartTexture);
            },
            error: (error) => {
                console.error('Error parsing CSV:', error);
            },
        });
    } catch (error) {
        console.error('Error loading CSV file:', error);
    }
};

// Create a THREE.CanvasTexture from the chart canvas
const createChartTexture = () => {
    renderChart(); // Render the chart to the canvas
    const texture = new THREE.CanvasTexture(chartCanvas);
    texture.minFilter = THREE.LinearFilter;
    texture.magFilter = THREE.LinearFilter;
    return texture;
};

const renderChart = () => {
    const chart = echarts.init(chartCanvas); // Initialize ECharts on the canvas

    const times = chartData.value.map((item) => item.Time);
    const values = chartData.value.map((item) => item.Value);

    const option = {
        backgroundColor: '#ffffff', // Set background color to white
        xAxis: {
            type: 'category',
            data: times,
        },
        yAxis: {
            type: 'value',
        },
        series: [
            {
                data: values,
                type: 'line',
            },
        ],
        graphic: [
            {
                type: 'rect',
                left: '0',
                top: '0',
                z: 1,
                shape: {
                    x: 0,
                    y: 0,
                    width: chartCanvas.width,
                    height: chartCanvas.height,
                },
                style: {
                    fill: 'none',
                    stroke: '#000000', // Border color
                    lineWidth: 2, // Border width
                },
            },
        ],
    };

    chart.setOption(option);
};

// 创建场景、创建相机
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 1, 2000);
camera.position.set(5, 5, 5);
scene.add(camera);

// 环境光
const ambientLight = new THREE.AmbientLight('white', 0.5);
scene.add(ambientLight);

const light = new THREE.DirectionalLight(0xffffff, 1);
scene.add(light);

const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);

// 控制器
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;

// xyz辅助坐标系
const axesHelper = new THREE.AxesHelper(5);
scene.add(axesHelper);

const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();
const spriteMap = new Map(); // 存储 Mesh 与 Sprite 的映射

const addHdr = () => {
    const rgbLoader = new RGBELoader();
    rgbLoader.loadAsync('/sea_2k.hdr').then((texture) => {
        texture.mapping = THREE.EquirectangularReflectionMapping; // 设置纹理映射方式
        scene.background = texture; // 将 HDR 贴图设置为场景背景
        scene.environment = texture; // 将 HDR 贴图设置为环境贴图
    }).catch((error) => {
        console.error('加载 HDR 贴图时出错', error);
    });
};

const addTexture = () => {
    const textureLoader = new THREE.TextureLoader().load('/textures/Wood_Deck__medium_1_0_0_baseColor.jpeg');
    textureLoader.mapping = THREE.EquirectangularRefractionMapping;
    return textureLoader;
};

// 创建带有文本的纹理
const createTextTexture = (text) => {
    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');
    context.font = '48px Arial';
    context.fillStyle = 'white';
    context.fillText(text, 0, 50);
    const texture = new THREE.CanvasTexture(canvas);
    return texture;
};


// const loadCSVData = async (url) => {
//     return new Promise((resolve, reject) => {
//         Papa.parse(url, {
//             download: true,
//             header: true,
//             complete: (results) => resolve(results.data),
//             error: (error) => reject(error)
//         });
//     });
// };

// 加载模型并添加到场景中
let model;
const addShip = () => {
    const gltfLoader = new GLTFLoader();
    gltfLoader.load(
        '/scene.gltf',
        (gltf) => {
            model = gltf.scene;
            model.scale.set(0.001, 0.001, 0.001);
            model.rotation.y = Math.PI / 2;
            model.position.z = 3.5;
            scene.add(model);

            // 遍历模型中的每个 Mesh 对象并为其添加 Sprite 标签
            model.traverse((child) => {
                if (child instanceof THREE.Mesh) {
                    const sprite = createSpriteForMesh(child);
                    scene.add(sprite);
                    spriteMap.set(child, sprite); // 将 Mesh 和 Sprite 关联起来
                }
            });

            controls.update();
        },
        undefined,
        (error) => {
            console.error('加载模型时出错', error);
        }
    );
};

// 创建与 Mesh 关联的 Sprite
// const createSpriteForMesh = (mesh) => {
//     const name = mesh.name || "Unnamed"; // 获取 Mesh 的 name 属性，如果没有则使用默认值
//     const texture = createTextTexture(name); // 使用 name 属性创建文本纹理
//     const spriteMaterial = new THREE.SpriteMaterial({ map: texture });
//     const sprite = new THREE.Sprite(spriteMaterial);

//     // 将 Sprite 放置在 Mesh 上方
//     sprite.position.copy(mesh.position);
//     sprite.position.y += 1; // 根据需要调整标签的高度
//     sprite.scale.set(1, 0.5, 1); // 根据需要调整标签的大小

//     // 初始状态下标签是隐藏的
//     sprite.visible = false;

//     return sprite;
// };


const createSpriteForMesh = (mesh) => {
    const name = mesh.name || "Unnamed"; // 获取 Mesh 的 name 属性，如果没有则使用默认值
    const texture = createTextTexture(name); // 使用 name 属性创建文本纹理
    const spriteMaterial = new THREE.SpriteMaterial({ map: texture });
    const sprite = new THREE.Sprite(spriteMaterial);
    sprite.name = name;

    // 计算 Mesh 的包围盒
    const boundingBox = new THREE.Box3().setFromObject(mesh);
    const boundingBoxSize = boundingBox.getSize(new THREE.Vector3());

    // 将 Sprite 放置在 Mesh 上方
    sprite.position.copy(boundingBox.max);
    sprite.position.x *= 0.0001; // 在包围盒顶部稍微向上偏移
    sprite.position.y *= 0.0001;
    sprite.position.y += 0.8;
    sprite.position.z *= 0.0001;
    sprite.scale.set(1, 0.5, 1); // 根据需要调整标签的大小

    // 初始状态下标签是隐藏的
    sprite.visible = false;

    return sprite;
};

// 监听鼠标点击事件
const onClick = async (event) => {
    event.preventDefault();

    // 将鼠标位置转化为归一化设备坐标
    mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
    mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

    // 通过射线检测点击的对象
    raycaster.setFromCamera(mouse, camera);
    const intersects = raycaster.intersectObjects(model.children, true);

    if (intersects.length > 0) {
        const mesh = intersects[0].object;
        const sprite = spriteMap.get(mesh);
        if (sprite) {
            if (!sprite.visible) {
                spriteMap.forEach((sprite) => {
                    sprite.visible = false;
                });
                sprite.visible = true;

                const chartTexture = createChartTexture();
                sprite.material.map = chartTexture;
                sprite.material.needsUpdate = true;
            } else {
                sprite.visible = false;
            }
            console.log(mesh.name)

        }


    }
};
let water;
const addWater = () => {
    // 创建水面
    const waterGeometry = new THREE.PlaneGeometry(100, 100);
    water = new Water(
        waterGeometry,
        {
            textureWidth: 512,
            textureHeight: 512,
            waterNormals: new THREE.TextureLoader().load('/Water.jpg', (texture) => {
                texture.wrapS = texture.wrapT = THREE.RepeatWrapping;
            }),
            sunDirection: new THREE.Vector3(),
            sunColor: 0xffffff,
            waterColor: 0xffffff,
            distortionScale: 3.7
        }
    );
    water.rotation.x = -Math.PI / 2;
    water.position.y = 0.15;
    scene.add(water);
};

// 添加事件监听
window.addEventListener('click', onClick);

// 渲染函数
const render = () => {
    renderer.render(scene, camera);
    water.material.uniforms['time'].value += 1.0 / 60.0;
    requestAnimationFrame(render);
};

// 生命周期钩子，确保在 setup 中调用
onMounted(async () => {
    await nextTick();
    loadCSVData();
    document.getElementById('home')?.appendChild(renderer.domElement);
    addHdr();
    addWater();
    addShip(); // 添加模型
    render(); // 启动渲染

});
</script>

<template>
    <!-- <div id="chart" style="width: 600px; height: 400px;"></div> -->
    <div id="home" class="w-full h-full"></div>

</template>
