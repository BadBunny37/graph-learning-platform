import * as THREE from 'three';

export function initThreeScene(containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const scene = new THREE.Scene();
    // Dark background to match CSS
    scene.background = new THREE.Color(0x0a0a0a);
    // Add some fog for depth
    scene.fog = new THREE.FogExp2(0x0a0a0a, 0.002);

    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.z = 30;

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    container.appendChild(renderer.domElement);

    // Create a network graph representation (Particles + Lines)
    const particlesGeometry = new THREE.BufferGeometry();
    const particlesCount = 700;

    const posArray = new Float32Array(particlesCount * 3);

    for (let i = 0; i < particlesCount * 3; i++) {
        // Spread particles in a wide area
        posArray[i] = (Math.random() - 0.5) * 100;
    }

    particlesGeometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3));

    // Material for dots
    const particlesMaterial = new THREE.PointsMaterial({
        size: 0.2,
        color: 0x00e5ff,
        transparent: true,
        opacity: 0.8,
    });

    const particlesMesh = new THREE.Points(particlesGeometry, particlesMaterial);
    scene.add(particlesMesh);

    // Lines connecting close particles
    const lineMaterial = new THREE.LineBasicMaterial({
        color: 0x7000ff,
        transparent: true,
        opacity: 0.15
    });

    // We will create lines dynamically in animation loop or pre-calculate
    // For performance, let's pre-calculate some lines between close points
    // Or better, use a simple wireframe sphere or similar structure to represent "data"

    const geometry = new THREE.IcosahedronGeometry(15, 2);
    const wireframe = new THREE.WireframeGeometry(geometry);
    const line = new THREE.LineSegments(wireframe);
    line.material.depthTest = false;
    line.material.opacity = 0.1;
    line.material.transparent = true;
    line.material.color = new THREE.Color(0x00e5ff);

    scene.add(line);

    // Add some floating geometric shapes to represent "documents" or "nodes"
    const group = new THREE.Group();
    const nodeGeo = new THREE.BoxGeometry(1, 1, 1);
    const nodeMat = new THREE.MeshBasicMaterial({ color: 0xff0055, wireframe: true });

    for (let i = 0; i < 10; i++) {
        const mesh = new THREE.Mesh(nodeGeo, nodeMat);
        mesh.position.x = (Math.random() - 0.5) * 40;
        mesh.position.y = (Math.random() - 0.5) * 40;
        mesh.position.z = (Math.random() - 0.5) * 40;
        mesh.rotation.x = Math.random() * Math.PI;
        mesh.rotation.y = Math.random() * Math.PI;
        group.add(mesh);
    }
    scene.add(group);

    // Mouse interaction
    let mouseX = 0;
    let mouseY = 0;

    function onDocumentMouseMove(event) {
        mouseX = (event.clientX - window.innerWidth / 2) * 0.05;
        mouseY = (event.clientY - window.innerHeight / 2) * 0.05;
    }

    document.addEventListener('mousemove', onDocumentMouseMove);

    // Handle Resize
    window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    });

    // Animation Loop
    const clock = new THREE.Clock();

    function animate() {
        requestAnimationFrame(animate);

        const elapsedTime = clock.getElapsedTime();

        // Rotate entire system slowly
        particlesMesh.rotation.y = elapsedTime * 0.05;
        line.rotation.y = elapsedTime * 0.05;
        line.rotation.x = elapsedTime * 0.02;

        // Rotate floating nodes
        group.rotation.y = elapsedTime * 0.1;
        group.children.forEach((child, i) => {
            child.rotation.x += 0.01;
            child.rotation.y += 0.01;
        });

        // Mouse parallax
        camera.position.x += (mouseX - camera.position.x) * 0.05;
        camera.position.y += (-mouseY - camera.position.y) * 0.05;
        camera.lookAt(scene.position);

        renderer.render(scene, camera);
    }

    animate();
}
