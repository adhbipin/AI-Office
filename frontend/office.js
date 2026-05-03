const scene = new THREE.Scene();
const camera = new THREE.OrthographicCamera(-12, 12, 12, -12, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
renderer.setSize(window.innerWidth * 0.7, window.innerHeight);
renderer.setPixelRatio(window.devicePixelRatio);
document.getElementById('canvas-container').appendChild(renderer.domElement);

camera.position.set(15, 15, 15);
camera.lookAt(0, 0, 0);

const ambientLight = new THREE.AmbientLight(0xffffff, 0.8);
scene.add(ambientLight);
const dirLight = new THREE.DirectionalLight(0xffffff, 0.6);
dirLight.position.set(10, 20, 10);
dirLight.castShadow = true;
scene.add(dirLight);

// Floor with grid
const floorGeo = new THREE.PlaneGeometry(24, 24);
const floorMat = new THREE.MeshLambertMaterial({ color: 0xeeeeee });
const floor = new THREE.Mesh(floorGeo, floorMat);
floor.rotation.x = -Math.PI / 2;
scene.add(floor);

const grid = new THREE.GridHelper(24, 24, 0xcccccc, 0xdddddd);
grid.position.y = 0.01;
scene.add(grid);

const DESK_POSITIONS = {
    pm:       { x:  0,   z: -6,  color: 0x2D9F77, name: 'Project Manager' },
    ui:       { x: -8,   z: -2,  color: 0x7F77DD, name: 'UI/UX Designer' },
    frontend: { x: -4,   z:  2,  color: 0x378ADD, name: 'Frontend Developer' },
    backend:  { x:  4,   z:  2,  color: 0xD85A30, name: 'Backend Developer' },
    qa:       { x:  8,   z: -2,  color: 0xBA7517, name: 'QA Engineer' },
    devops:   { x:  0,   z:  6,  color: 0x639922, name: 'DevOps Engineer' },
};

const avatars = {};
const particles = [];

function createAvatar(color) {
    const group = new THREE.Group();
    const mat = new THREE.MeshLambertMaterial({ color });
    
    // Head
    const head = new THREE.Mesh(new THREE.SphereGeometry(0.4, 16, 16), mat);
    head.position.y = 2.0;
    
    // Torso
    const torso = new THREE.Mesh(new THREE.BoxGeometry(0.7, 1.0, 0.4), mat);
    torso.position.y = 1.3;
    
    // Arms
    const armGeo = new THREE.CylinderGeometry(0.1, 0.1, 0.7);
    const leftArm = new THREE.Mesh(armGeo, mat);
    leftArm.position.set(-0.5, 1.4, 0);
    leftArm.rotation.z = 0.5;
    
    const rightArm = new THREE.Mesh(armGeo, mat);
    rightArm.position.set(0.5, 1.4, 0);
    rightArm.rotation.z = -0.5;
    
    group.add(head, torso, leftArm, rightArm);
    return group;
}

Object.entries(DESK_POSITIONS).forEach(([key, pos]) => {
    // Desk
    const desk = new THREE.Mesh(
        new THREE.BoxGeometry(2.5, 0.1, 1.5),
        new THREE.MeshLambertMaterial({ color: pos.color })
    );
    desk.position.set(pos.x, 0.8, pos.z);
    scene.add(desk);

    const legGeo = new THREE.CylinderGeometry(0.05, 0.05, 0.8);
    const legMat = new THREE.MeshLambertMaterial({ color: 0x333333 });
    [[-1.1, -0.6], [1.1, -0.6], [-1.1, 0.6], [1.1, 0.6]].forEach(offset => {
        const leg = new THREE.Mesh(legGeo, legMat);
        leg.position.set(pos.x + offset[0], 0.4, pos.z + offset[1]);
        scene.add(leg);
    });

    // Avatar
    const avatar = createAvatar(pos.color);
    avatar.position.set(pos.x, 0, pos.z - 1); // Sit behind desk
    scene.add(avatar);
    avatars[key] = avatar;
    avatar.userData = { originalY: 0, bobSpeed: 0.002 + Math.random() * 0.001 };
});

class Particle {
    constructor(startPos, endPos, color) {
        this.mesh = new THREE.Mesh(
            new THREE.SphereGeometry(0.15, 8, 8),
            new THREE.MeshBasicMaterial({ color, transparent: true, opacity: 0.8 })
        );
        scene.add(this.mesh);
        
        this.start = startPos.clone();
        this.end = endPos.clone();
        this.progress = 0;
        this.speed = 0.02;
    }

    update() {
        this.progress += this.speed;
        if (this.progress > 1) {
            scene.remove(this.mesh);
            return false;
        }
        
        // Arc movement
        const currentPos = new THREE.Vector3().lerpVectors(this.start, this.end, this.progress);
        currentPos.y += Math.sin(this.progress * Math.PI) * 3;
        this.mesh.position.copy(currentPos);
        return true;
    }
}

function spawnParticle(fromKey, toKey) {
    const fromPos = avatars[fromKey].position;
    const toPos = (toKey === 'All' || !avatars[toKey]) ? new THREE.Vector3(0, 5, 0) : avatars[toKey].position;
    const color = DESK_POSITIONS[fromKey].color;
    particles.push(new Particle(fromPos, toPos, color));
}

function showSpeechBubble(agentKey, message) {
    const avatar = avatars[agentKey];
    if (!avatar) return;
    
    // Project 3D to 2D
    const vector = new THREE.Vector3(avatar.position.x, avatar.position.y + 2.5, avatar.position.z);
    vector.project(camera);
    
    const x = (vector.x * 0.5 + 0.5) * window.innerWidth * 0.7;
    const y = (-vector.y * 0.5 + 0.5) * window.innerHeight;

    const div = document.createElement('div');
    div.className = 'speech-bubble';
    div.style.left = x + 'px';
    div.style.top = y + 'px';
    div.innerText = message.length > 50 ? message.substring(0, 50) + '...' : message;
    document.body.appendChild(div);
    
    setTimeout(() => {
        div.style.opacity = '0';
        setTimeout(() => div.remove(), 500);
    }, 3000);
}

function animate(time) {
    requestAnimationFrame(animate);
    
    // Bobbing animation
    Object.values(avatars).forEach(avatar => {
        avatar.position.y = avatar.userData.originalY + Math.sin(time * avatar.userData.bobSpeed) * 0.1;
    });

    // Particles
    for (let i = particles.length - 1; i >= 0; i--) {
        if (!particles[i].update()) {
            particles.splice(i, 1);
        }
    }

    TWEEN.update(time);
    renderer.render(scene, camera);
}

window.addEventListener('resize', () => {
    renderer.setSize(window.innerWidth * 0.7, window.innerHeight);
    camera.updateProjectionMatrix();
});

animate();
