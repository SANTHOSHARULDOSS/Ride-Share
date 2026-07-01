/* ==========================================================================
   Ride Share Client Application logic & PWA handlers
   ========================================================================== */

// Service Worker Registration
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js')
      .then((reg) => {
        console.log('[Service Worker] Registered successfully with scope:', reg.scope);
      })
      .catch((err) => {
        console.error('[Service Worker] Registration failed:', err);
      });
  });
}

// PWA Install Prompt Handler
let deferredPrompt;
const installBtn = document.getElementById('pwa-install-btn');

window.addEventListener('beforeinstallprompt', (e) => {
  // Prevent default install bar
  e.preventDefault();
  // Save event
  deferredPrompt = e;
  // Show install button
  if (installBtn) {
    installBtn.classList.remove('d-none');
  }
});

if (installBtn) {
  installBtn.addEventListener('click', async () => {
    if (!deferredPrompt) return;
    // Show prompt
    deferredPrompt.prompt();
    // Wait for choice
    const { outcome } = await deferredPrompt.userChoice;
    console.log(`[PWA] User response to install: ${outcome}`);
    // Reset prompt
    deferredPrompt = null;
    // Hide button
    installBtn.classList.add('d-none');
  });
}

// Network Status Observers
const offlineBanner = document.createElement('div');
offlineBanner.className = 'offline-banner';
offlineBanner.innerHTML = `<i class="fa-solid fa-wifi-slash"></i> You are offline. Running in Offline Demo Mode.`;
document.body.appendChild(offlineBanner);

function updateConnectionStatus() {
  if (navigator.onLine) {
    offlineBanner.style.display = 'none';
  } else {
    offlineBanner.style.display = 'flex';
    // Automatically fall back map queries or show demo mode alerts
    const statusBanners = document.querySelectorAll('.demo-status-badge');
    statusBanners.forEach(badge => {
      badge.textContent = 'Demo Mode (Offline)';
      badge.className = 'badge bg-warning text-dark demo-status-badge';
    });
  }
}

window.addEventListener('online', updateConnectionStatus);
window.addEventListener('offline', updateConnectionStatus);
// Initial check
updateConnectionStatus();

// SOS Trigger Simulation
function triggerSOS(rideId, driverName) {
  // Play a mock sound
  try {
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const oscillator = audioContext.createOscillator();
    const gainNode = audioContext.createGain();
    
    oscillator.type = 'sawtooth';
    oscillator.frequency.setValueAtTime(880, audioContext.currentTime); // A5 note (piercing siren)
    oscillator.connect(gainNode);
    gainNode.connect(audioContext.destination);
    
    // Siren effect
    oscillator.frequency.linearRampToValueAtTime(440, audioContext.currentTime + 0.4);
    oscillator.frequency.linearRampToValueAtTime(880, audioContext.currentTime + 0.8);
    
    gainNode.gain.setValueAtTime(0.1, audioContext.currentTime);
    gainNode.gain.linearRampToValueAtTime(0.01, audioContext.currentTime + 0.8);
    
    oscillator.start();
    oscillator.stop(audioContext.currentTime + 0.8);
  } catch (e) {
    console.log("Audio siren failed to play (user gesture required):", e);
  }

  // Display notification/alert
  alert(`🚨 SOS EMERGENCY TRIGGERED! 🚨\n\nRide ID: ${rideId}\nDriver: ${driverName}\n\nEmergency services notified (simulated). GPS coordinates transmitted.`);
  console.log(`SOS Alert Sent for Ride ${rideId} by Driver ${driverName}`);
}

// Leaflet Map Marker Animation
let animationInterval;
function animateDriverMovement(map, marker, waypoints, onStepCallback, onCompleteCallback) {
  if (waypoints.length < 2) return;
  if (animationInterval) clearInterval(animationInterval);

  let currentSegment = 0;
  let t = 0; // Interpolation factor (0 to 1)
  const stepsPerSegment = 20; // Number of steps between waypoints
  const stepTimeMs = 300; // Time per step

  animationInterval = setInterval(() => {
    const startWp = waypoints[currentSegment];
    const endWp = waypoints[currentSegment + 1];

    if (!startWp || !endWp) {
      clearInterval(animationInterval);
      if (onCompleteCallback) onCompleteCallback();
      return;
    }

    // Linearly interpolate coordinates
    const lat = startWp.lat + (endWp.lat - startWp.lat) * (t / stepsPerSegment);
    const lng = startWp.lng + (endWp.lng - startWp.lng) * (t / stepsPerSegment);

    // Update marker position
    const newPos = L.latLng(lat, lng);
    marker.setLatLng(newPos);
    
    // Pan map to follow
    map.panTo(newPos);

    if (onStepCallback) {
      onStepCallback(lat, lng, endWp.name);
    }

    t++;
    if (t > stepsPerSegment) {
      t = 0;
      currentSegment++;
      if (currentSegment >= waypoints.length - 1) {
        clearInterval(animationInterval);
        if (onCompleteCallback) onCompleteCallback();
      }
    }
  }, stepTimeMs);
}
