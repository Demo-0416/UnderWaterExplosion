<template>
    <div id="three-container"></div>
</template>

<script>
import * as THREE from 'three';
import { MMDLoader } from 'three/examples/jsm/loaders/MMDLoader.js';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { Chart, registerables } from 'chart.js'; // 正确导入 Chart.js
Chart.register(...registerables); // 注册所有需要的组件

export default {
    mounted() {
        // 创建场景、摄像机和渲染器
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ antialias: true });

        // 设置渲染器的大小
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.getElementById('three-container').appendChild(renderer.domElement);

        // 设置光源
        const hemiLight = new THREE.HemisphereLight(0xffffff, 0x444444);
        const HemisphereLight = new THREE.HemisphereLight(0xffffff, 0x080820, .5)
        hemiLight.position.set(0, 200, 0);
        scene.add(HemisphereLight);

        const dirLight = new THREE.DirectionalLight(0xffffff);
        dirLight.position.set(0, 200, 100);
        dirLight.castShadow = true;
        scene.add(dirLight);

        // 使用 MMDLoader 加载 PMX 模型
        const loader = new MMDLoader();
        loader.load(
            '/models/boat.pmx',
            (model) => {
                scene.add(model);

                // 在模型上方添加悬浮窗
                addFloatingWindow(scene, model);
                animate(); // 开始动画循环
            },
            undefined,
            (error) => {
                console.error('加载 PMX 模型时出错', error);
            }
        );

        // 设置摄像机位置
        camera.position.set(0, 10, 50);

        // 轨道控制器
        const controls = new OrbitControls(camera, renderer.domElement);
        controls.target.set(0, 10, 0);
        controls.update();

        // 动画循环函数
        function animate() {
            requestAnimationFrame(animate);
            controls.update();
            renderer.render(scene, camera);
        }

        // 处理窗口大小变化
        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        });

        // 添加悬浮窗的函数
        function addFloatingWindow(scene, model) {
            // 创建一个Canvas元素用于绘制时序图
            const canvas = document.createElement('canvas');
            canvas.width = 512;
            canvas.height = 256;

            // 将Canvas作为材质应用到Sprite上
            const texture = new THREE.CanvasTexture(canvas);
            const material = new THREE.SpriteMaterial({ map: texture });
            const sprite = new THREE.Sprite(material);

            // 绘制时序图
            const ctx = canvas.getContext('2d');
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
                    datasets: [{
                        label: 'Sample Data',
                        data: [65, 59, 80, 81, 56, 55, 40],
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 2,
                        fill: false,
                    }],
                },
                options: {
                    responsive: false,
                    maintainAspectRatio: false,
                },
            });

            // 设置Sprite的位置
            sprite.scale.set(10, 5, 1); // 控制悬浮窗的大小
            sprite.position.set(0, 20, 0); // 悬浮窗位于模型上方

            // 将Sprite添加到场景中
            scene.add(sprite);
        }
    },
};
</script>

<style scoped>
#three-container {
    width: 100%;
    height: 100vh;
    /* 全屏显示 */
    overflow: hidden;
    margin: 0;
    padding: 0;
}
</style>
