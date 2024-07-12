<template>
    <div ref="floatDrag" class="float-position" id="float-box"
        :style="{ left: left + 'px', top: top + 'px', right: right + 'px !important', zIndex: zIndex }" @touchmove.prevent
        @mousemove.prevent @mousedown="mouseDown" @mouseup="mouseUp">
        <div class="drag">
            <svg t="1682058484158" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="2023" width="32" height="32"><path d="M556.297 172.715a42.407 42.407 0 0 1 42.426 42.398l0.837 267.69c-0.118 1.703 0.63 2.737 1.408 2.737 0.63 0 1.29-0.699 1.506-2.284l37.74-208.953c3.732-20.672 21.844-36.166 42.162-36.166a40.074 40.074 0 0 1 7.136 0.64c23.064 4.164 38.391 27.562 34.217 50.587l-33.656 244.529c0 2.559 0.483 4.478 1.32 4.478 0.58 0 1.328-0.935 2.175-3.218l50.144-134.063c6.27-17.65 23.034-29.403 40.793-29.403A39.798 39.798 0 0 1 797.892 374c22.08 7.875 33.626 33.41 25.78 55.47l-87.904 287.191c-0.453 1.585-0.984 3.16-1.437 4.725l-0.187 0.591v0.128a187.031 187.031 0 0 1-177.847 129.1c-53.156 0-108.42-18.752-150.472-51-45.419-27.336-190.968-183.783-190.968-183.783-22.09-22.07-18.792-55.882 3.297-77.962 11.537-11.537 25.919-17.6 40.173-17.6 13.033 0 25.967 5.05 36.51 15.592l63.138 63.157c8.603 8.594 18.132 12.699 26.922 12.699a26.952 26.952 0 0 0 20.88-9.893c7.658-9.037 4.635-36.914 2.49-54.594l-31.668-260.259c-2.825-23.26 13.781-45.724 37.003-48.549a40.497 40.497 0 0 1 4.853-0.295c21.282 0 39.749 16.98 42.387 38.597l34.926 204.425c0.905 2.54 2.342 4.036 3.602 4.036s2.353-1.496 2.58-4.922l11.88-265.741a42.417 42.417 0 0 1 42.467-42.398m0-70.875a113.36 113.36 0 0 0-104.344 69.153c-0.246 0.57-0.482 1.152-0.718 1.732a111.234 111.234 0 0 0-90.022 10.976 113.597 113.597 0 0 0-32.415 29.207 115.23 115.23 0 0 0-19.067 38.489 113.843 113.843 0 0 0-3.465 44.68l21.36 175.77a120.842 120.842 0 0 0-69.3-21.863c-33.468 0-65.549 13.614-90.286 38.332-23.212 23.202-36.993 53.363-38.863 84.952a120.92 120.92 0 0 0 34.502 92.216c5.532 5.906 39.64 42.407 79.203 82.412 74.586 75.422 105.328 99.648 122.702 110.771 53.973 40.36 123.254 63.414 190.674 63.414A257.906 257.906 0 0 0 801.14 745.1c0.247-0.709 0.483-1.417 0.7-2.136l0.117-0.374a178.56 178.56 0 0 0 1.723-5.64l87.413-285.578a113.203 113.203 0 0 0 5.729-42.86 115.585 115.585 0 0 0-35.772-77.135 111.431 111.431 0 0 0-67.45-30.19l0.148-0.985a113.676 113.676 0 0 0-1.201-43.155 115.408 115.408 0 0 0-16.872-39.523 113.774 113.774 0 0 0-30.703-30.968 111.077 111.077 0 0 0-84.981-17.06 113.203 113.203 0 0 0-103.694-67.656z" fill="#ffffff" p-id="2024"></path></svg>
        </div>
        <div class="content" id="content" @click="handelFlex">
            <!-- <img src="../../../../assets/image/alarm.png" alt="" /> -->
            <div class="label">
                <div v-if="flag">展开</div>
                <div v-else>收起</div>
            </div>
            <div class="item-container">
                <div v-for="(item, index) in powerList" :key="index" @click.stop="activeHandle(index)"
                    >
                    <div :class="activeIndex == index ? 'active power-item' : 'power-item'">
                        <img :src="item.path" alt="" style="width: 26px"/>
                    </div>
                    <div :class="activeIndex == index ? 'active-des des' : 'des'">{{ item.label }}</div>
                </div>
            </div>
        </div>
    </div>
</template>
    
<script>
export default {
    name: 'DragBall',
    props: {
        distanceRight: {
            type: Number,
            default: 36,
        },
        distanceBottom: {
            type: Number,
            default: 700,
        },
        isScrollHidden: {
            type: Boolean,
            default: false,
        },
        isCanDraggable: {
            type: Boolean,
            default: true,
        },
        zIndex: {
            type: Number,
            default: 50,
        },
        value: {
            type: String,
            default: '悬浮球！',
        },
    },
    data() {
        return {
            clientWidth: null,
            clientHeight: null,
            left: null,
            top: null,
            right: null,
            timer: null,
            currentTop: 0,
            mousedownX: 0,
            mousedownY: 0,

            flag: true, // 控制悬浮框是否展开
            box: '', // 悬浮球的dom
            activeIndex: null, //高亮显示
            powerList: [
                {
        path: '/favicon.ico',
                    label: '个人'
                },
                {
        path: '/favicon.ico',
                    label: '选择试验'
                },
                
            ]
        };
    },
    created() {
        this.clientWidth = document.documentElement.clientWidth;
        this.clientHeight = document.documentElement.clientHeight;
    },
    mounted() {
        this.isCanDraggable &&
            this.$nextTick(() => {
                this.floatDrag = this.$refs.floatDrag;
                // 获取元素位置属性
                this.floatDragDom = this.floatDrag.getBoundingClientRect();
                // 设置初始位置
                // this.left = this.clientWidth - this.floatDragDom.width - this.distanceRight;
                this.right = 0;
                this.top = this.clientHeight - this.floatDragDom.height - this.distanceBottom;
                this.initDraggable();
            });
        // this.isScrollHidden && window.addEventListener('scroll', this.handleScroll);
        window.addEventListener('resize', this.handleResize);

        this.box = document.getElementById("float-box")
    },
    beforeUnmount() {
        window.removeEventListener('scroll', this.handleScroll);
        window.removeEventListener('resize', this.handleResize);
    },
    methods: {
        // 伸缩悬浮球
        handelFlex() {
            if (this.flag) {
                this.buffer(this.box, "height", 220);
            } else {
                this.buffer(this.box, "height", 70);
            }
            this.flag = !this.flag
            console.log('是否展开', this.flag)
        },
        // 点击哪个power
        activeHandle(index) {
            //把我们自定义的下标赋值
            this.activeIndex = index
            console.log('HHHH', index)
        },
        // 获取要改变得样式属性
        getStyleAttr(obj, attr) {
            if (obj.currentStyle) {
                // IE 和 opera
                return obj.currentStyle[attr];
            } else {
                return window.getComputedStyle(obj, null)[attr];
            }
        },
        // 动画函数
        buffer(eleObj, attr, target) {
            // setInterval方式开启动画
            //先清后设
            // clearInterval(eleObj.timer);
            // let speed = 0
            // let begin = 0
            // //设置定时器
            // eleObj.timer = setInterval(() => {
            //     //获取动画属性的初始值
            //     begin = parseInt(this.getStyleAttr(eleObj, attr));
            //     speed = (target - begin) * 0.2;
            //     speed = target > begin ? Math.ceil(speed) : Math.floor(speed);
            //     eleObj.style[attr] = begin + speed + "px";
            //     if (begin === target) {
            //         clearInterval(eleObj.timer);
            //     }
            // }, 20);
            // cancelAnimationFrame开启动画
            // 先清后设
            cancelAnimationFrame(eleObj.timer)
            let speed = 0
            let begin = 0
            let _this = this
            eleObj.timer = requestAnimationFrame(function fn() {
                begin = parseInt(_this.getStyleAttr(eleObj, attr))
                // 动画速度
                speed = (target - begin) * 0.9
                speed = target > begin ? Math.ceil(speed) : Math.floor(speed)
                eleObj.style[attr] = begin + speed + "px"
                eleObj.timer = requestAnimationFrame(fn)
                if (begin === target) {
                    cancelAnimationFrame(eleObj.timer);
                }
            })
        },
        /**
         * 窗口resize监听
         */
        handleResize() {
            // this.clientWidth = document.documentElement.clientWidth;
            // this.clientHeight = document.documentElement.clientHeight;
            // console.log(window.innerWidth);
            // console.log(document.documentElement.clientWidth);


            this.checkDraggablePosition();
        },
        /**
         * 初始化draggable
         */
        initDraggable() {
            this.floatDrag.addEventListener('touchstart', this.toucheStart);
            this.floatDrag.addEventListener('touchmove', (e) => this.touchMove(e));
            this.floatDrag.addEventListener('touchend', this.touchEnd);
        },
        mouseDown(e) {
            const event = e || window.event;
            this.mousedownX = event.screenX;
            this.mousedownY = event.screenY;
            const that = this;
            let floatDragWidth = this.floatDragDom.width / 2;
            let floatDragHeight = this.floatDragDom.height / 2;
            if (event.preventDefault) {
                event.preventDefault();
            }
            this.canClick = false;
            this.floatDrag.style.transition = 'none';
            document.onmousemove = function (e) {
                var event = e || window.event;
                that.left = event.clientX - floatDragWidth;
                that.top = event.clientY - floatDragHeight;
                if (that.left < 0) that.left = 0;
                if (that.top < 0) that.top = 0;
                // 鼠标移出可视区域后给按钮还原
                if (
                    event.clientY < 0 ||
                    event.clientY > Number(this.clientHeight) ||
                    event.clientX > Number(this.clientWidth) ||
                    event.clientX < 0
                ) {
                    this.right = 0;
                    this.top = this.clientHeight - this.floatDragDom.height - this.distanceBottom;
                    document.onmousemove = null;
                    this.floatDrag.style.transition = 'all 0.3s';
                    return;
                }
                if (that.left >= document.documentElement.clientWidth - floatDragWidth * 2) {
                    that.left = document.documentElement.clientWidth - floatDragWidth * 2;
                }
                if (that.top >= that.clientHeight - floatDragHeight * 2) {
                    that.top = that.clientHeight - floatDragHeight * 2;
                }
            };
        },
        mouseUp(e) {
            const event = e || window.event;
            //判断只是单纯的点击，没有拖拽
            if (this.mousedownY == event.screenY && this.mousedownX == event.screenX) {
                this.$emit('handlepaly');
            }
            document.onmousemove = null;
            this.checkDraggablePosition();
            this.floatDrag.style.transition = 'all 0.3s';
        },
        toucheStart() {
            this.canClick = false;
            this.floatDrag.style.transition = 'none';
        },
        touchMove(e) {
            this.canClick = true;
            if (e.targetTouches.length === 1) {
                // 单指拖动
                let touch = event.targetTouches[0];
                this.left = touch.clientX - this.floatDragDom.width / 2;
                this.top = touch.clientY - this.floatDragDom.height / 2;
            }
        },
        touchEnd() {
            if (!this.canClick) return; // 解决点击事件和touch事件冲突的问题
            this.floatDrag.style.transition = 'all 0.3s';
            this.checkDraggablePosition();
        },
        /**
         * 判断元素显示位置
         * 在窗口改变和move end时调用
         */
        checkDraggablePosition() {
            this.clientWidth = document.documentElement.clientWidth;
            this.clientHeight = document.documentElement.clientHeight;
            if (this.left + this.floatDragDom.width / 2 >= this.clientWidth / 2) {
                // 判断位置是往左往右滑动
                this.left = this.clientWidth - this.floatDragDom.width;
            } else {
                this.left = 0;
            }
            if (this.top < 0) {
                // 判断是否超出屏幕上沿
                this.top = 0;
            }
            if (this.top + this.floatDragDom.height >= this.clientHeight) {
                // 判断是否超出屏幕下沿
                this.top = this.clientHeight - this.floatDragDom.height;
            }
        },
    },
};
</script>
<style>
html,
body {
    overflow: hidden;
}
</style>
<style scoped lang="scss">
.float-position {
    position: fixed;
    z-index: 10003 !important;
    left: 0;
    top: 20%;
    width: 70px;
    height: 70px;
    border-radius: 32px;
    // background: rgba(167, 160, 161, .5);
    cursor: pointer;
    overflow: hidden;
    user-select: none;

    display: block;
    background: black;
    // border-radius: 50%;
    margin: 0;
    background: -webkit-radial-gradient(100px 100px, circle, #35a1a1, #000);
    background: -moz-radial-gradient(100px 100px, circle, #35a1a1, #000);
    background: radial-gradient(100px 100px, circle, #35a1a1, #000);
    .drag {
        width: 70px;
        height: 35px;
        // background: #f2e96a;
        text-align: center;
        line-height: 35px;
        border-bottom: 1px solid #fff;
    }
    .content {
        width: 70px;
        height: 35px;
        // background: #716af2;
        .label {
            width: 70px;
            height: 35px;
            text-align: center;
            line-height: 35px;
            color: white;
        }
        .label:hover {
            color: rgb(243, 82, 19);
            transition: all 0.5;
        }

        .item-container {
            margin-top: 10px;
            width: 70px;
            height: 600px;
            display: flex;
            //justify-content: space-between;
            align-items: center;
            flex-direction: column;

            .power-item {
                width: 40px;
                height: 40px;
                border-radius: 50%;
                background-color: #69707a;
                display: flex;
                justify-content: center;
                align-items: center;
                flex-direction: column;
            }
            .des {
                width: 40px;
                text-align: center;
                margin-bottom: 5px;
                font-size: 10px;
                color: #fff;
            }
        }
    }

    .close {
        width: 20px;
        height: 20px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #fff;
        background: rgba(0, 0, 0, 0.6);
        position: absolute;
        right: -10px;
        top: -12px;
        cursor: pointer;
    }
}

.cart {
    border-radius: 50%;
    width: 5em;
    height: 5em;
    display: flex;
    align-items: center;
    justify-content: center;
}

.header-notice {
    display: inline-block;
    transition: all 0.3s;

    span {
        vertical-align: initial;
    }

    .notice-badge {
        color: inherit;

        .header-notice-icon {
            font-size: 16px;
            padding: 4px;
        }
    }
}

.drag-ball .drag-content {
    overflow-wrap: break-word;
    font-size: 14px;
    color: #fff;
    letter-spacing: 2px;
}

.active {
    background-color: #1a1818 !important;
    
}
.active-des {
    color: #1a1818 !important;
    font-weight: bold !important;
}
</style>
