import '../src/css/style.css'
import { initThreeScene } from './js/three-scene.js'

// Initialize 3D Scene if container exists
if (document.getElementById('canvas-container')) {
  initThreeScene('canvas-container');
} else if (document.getElementById('graph-container')) {
  initThreeScene('graph-container');
}

// Global UI Interactions (if any)
console.log('GraphLearn App Initialized');
