document.addEventListener('DOMContentLoaded', () => {
    const touchArea = document.getElementById('touch-area');
    const outputDiv = document.getElementById('output');

    let touchStartTime = 0;
    let startX = 0;
    let startY = 0;
    const SWIPE_THRESHOLD = 50; // pixels
    const LONG_PRESS_THRESHOLD = 500; // milliseconds

    function logAction(action) {
        outputDiv.textContent = `Action: ${action}`;
        console.log(`Action: ${action}`);
    }

    touchArea.addEventListener('touchstart', (e) => {
        e.preventDefault(); // Prevent default browser touch behaviors
        touchArea.classList.add('active'); // Visual feedback
        touchStartTime = Date.now();
        if (e.touches.length === 1) { // Only care about single touches for this demo
            startX = e.touches[0].clientX;
            startY = e.touches[0].clientY;
        }
    });

    touchArea.addEventListener('touchend', (e) => {
        e.preventDefault();
        touchArea.classList.remove('active'); // Visual feedback

        const touchDuration = Date.now() - touchStartTime;

        if (e.changedTouches.length === 1) {
            const endX = e.changedTouches[0].clientX;
            const endY = e.changedTouches[0].clientY;

            const deltaX = endX - startX;
            const deltaY = endY - startY;

            // Check for tap (short duration, minimal movement)
            if (touchDuration < LONG_PRESS_THRESHOLD && Math.abs(deltaX) < 10 && Math.abs(deltaY) < 10) {
                logAction('Tap Detected! (Trigger primary action)');
                // Example: Toggle a light, open a small menu
                return;
            }

            // Check for long press
            if (touchDuration >= LONG_PRESS_THRESHOLD && Math.abs(deltaX) < 10 && Math.abs(deltaY) < 10) {
                logAction('Long Press Detected! (Trigger secondary/contextual action)');
                // Example: Open a context menu, show details
                return;
            }

            // Check for swipe
            if (Math.abs(deltaX) > SWIPE_THRESHOLD || Math.abs(deltaY) > SWIPE_THRESHOLD) {
                if (Math.abs(deltaX) > Math.abs(deltaY)) { // Horizontal swipe
                    if (deltaX > 0) {
                        logAction('Swipe Right! (Next item, navigate forward)');
                        // Example: Navigate to next page/item, close current panel
                    } else {
                        logAction('Swipe Left! (Previous item, navigate back)');
                        // Example: Navigate to previous page/item, open new panel
                    }
                } else { // Vertical swipe
                    if (deltaY > 0) {
                        logAction('Swipe Down! (Scroll down, refresh content)');
                        // Example: Scroll content, pull-to-refresh
                    } else {
                        logAction('Swipe Up! (Scroll up, open quick settings)');
                        // Example: Scroll content, dismiss notification
                    }
                }
                return;
            }
        }
        logAction('Touch interaction completed.');
    });

    touchArea.addEventListener('touchmove', (e) => {
        e.preventDefault(); // Prevent scrolling/zooming during a drag
        // You could add logic here for real-time drag feedback
    });
});
