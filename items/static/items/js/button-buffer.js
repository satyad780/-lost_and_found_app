(function () {
    'use strict';

    function onActivate(e) {
        // Handle both click and keyboard activation
        const el = e.currentTarget;
        const href = el.getAttribute('href');
        const minDelay = Math.max(0, parseFloat(el.dataset.bufferSeconds) || 3) * 1000;
        const maxFetchTimeout = parseInt(el.dataset.fetchTimeoutMs, 10) || 10000; // ms

        if (el.classList.contains('is-buffering')) return;
        e.preventDefault();

        // Mark button busy
        el.classList.add('is-buffering');
        el.setAttribute('aria-busy', 'true');
        el.setAttribute('aria-disabled', 'true');

        // Show the full-page loader overlay
        var loader = document.getElementById('page-loader');
        var cancelBtn = loader ? loader.querySelector('.loader-cancel') : null;
        if (loader) {
            loader.classList.add('active');
            loader.setAttribute('aria-hidden', 'false');
            // make focusable and focus it (or the cancel button)
            loader.setAttribute('tabindex', '-1');
            if (cancelBtn) cancelBtn.focus(); else loader.focus();
            // prevent scrolling
            document.body.style.overflow = 'hidden';
        }

        // Setup abortable fetch and state
        var controller = new AbortController();
        el._bufferController = controller; // keep reference for cleanup
        var didFetch = false;
        var fetchError = false;
        var navigated = false;

        // Helper to navigate once both minDelayElapsed and fetch succeeded (full body read) or timeout/error
        function maybeNavigate() {
            if (navigated) return;
            if (minDone && (didFetch || fetchError || fetchTimedOut)) {
                navigated = true;
                // cleanup before navigation
                cleanup();
                // restore scrolling before navigation
                document.body.style.overflow = '';
                window.location.href = href;
            }
        }

        // Start min delay
        var minDone = false;
        setTimeout(function () {
            minDone = true;
            maybeNavigate();
        }, minDelay);

        // Start fetch with timeout; wait for full body text
        var fetchTimer = setTimeout(function () {
            fetchTimedOut = true;
            // allow navigation to proceed after minDone
            maybeNavigate();
        }, maxFetchTimeout);
        var fetchTimedOut = false;

        fetch(href, { method: 'GET', credentials: 'same-origin', signal: controller.signal })
            .then(function (resp) {
                if (!resp.ok) { fetchError = true; return; }
                return resp.text().then(function () { didFetch = true; });
            })
            .catch(function (err) {
                fetchError = true;
            })
            .finally(function () {
                clearTimeout(fetchTimer);
                maybeNavigate();
            });

        // Cancel button handler
        function cancelLoad() {
            controller.abort();
            cleanup();
            // hide loader and restore button state
            if (loader) {
                loader.classList.remove('active');
                loader.setAttribute('aria-hidden', 'true');
                loader.removeAttribute('tabindex');
            }
            el.classList.remove('is-buffering');
            el.removeAttribute('aria-busy');
            el.removeAttribute('aria-disabled');
            if (cancelBtn && cancelBtn._bufferCancelHandler) {
                cancelBtn.removeEventListener('click', cancelBtn._bufferCancelHandler);
                delete cancelBtn._bufferCancelHandler;
            }
            document.removeEventListener('keydown', escHandler);
            document.body.style.overflow = '';
            // return focus to the button
            el.focus();
            // clear stored controller reference
            try { delete el._bufferController; } catch (e) {}
        }

        function escHandler(ev) {
            if (ev.key === 'Escape') cancelLoad();
        }

        function cleanup() {
            try { clearTimeout(fetchTimer); } catch (e) {}
            if (el._bufferController) {
                try { el._bufferController.abort(); } catch (e) {}
                try { delete el._bufferController; } catch (e) {}
            }
        }

        if (cancelBtn) {
            cancelBtn._bufferCancelHandler = cancelLoad;
            cancelBtn.addEventListener('click', cancelLoad);
        }
        document.addEventListener('keydown', escHandler);
    }

    function addButtonBehaviour(btn) {
        // Only attach behavior to anchor links (we don't want to intercept form submit buttons)
        if (btn.tagName && btn.tagName.toLowerCase() !== 'a') return;
        if (!btn.getAttribute('href')) return;

        // ensure label exists
        if (!btn.querySelector('.btn-label')) {
            var label = document.createElement('span');
            label.className = 'btn-label';
            label.textContent = btn.textContent.trim();
            btn.textContent = '';
            btn.appendChild(label);
        }

        btn.addEventListener('click', onActivate);
        btn.addEventListener('keydown', function (e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                btn.click();
            }
        });
    }

    document.addEventListener('DOMContentLoaded', function () {
        var buttons = document.querySelectorAll('.btn-report');
        buttons.forEach(addButtonBehaviour);
        // Ensure loader/controls are reset when page is first loaded
        resetOverlay();
    });

    // Reset overlay and abort any pending buffers (useful when coming back via Back navigation / bfcache)
    function resetOverlay() {
        var loader = document.getElementById('page-loader');
        if (loader) {
            loader.classList.remove('active');
            loader.setAttribute('aria-hidden', 'true');
            loader.removeAttribute('tabindex');
        }
        document.body.style.overflow = '';

        var buttons = document.querySelectorAll('.btn-report.is-buffering');
        buttons.forEach(function (btn) {
            btn.classList.remove('is-buffering');
            btn.removeAttribute('aria-busy');
            btn.removeAttribute('aria-disabled');

            if (btn._bufferController) {
                try { btn._bufferController.abort(); } catch (e) {}
                try { delete btn._bufferController; } catch (e) {}
            }
        });

        var cancelBtn = document.querySelector('#page-loader .loader-cancel');
        if (cancelBtn && cancelBtn._bufferCancelHandler) {
            try { cancelBtn.removeEventListener('click', cancelBtn._bufferCancelHandler); } catch (e) {}
            try { delete cancelBtn._bufferCancelHandler; } catch (e) {}
        }
    }

    // When a page is restored from bfcache, pageshow fires with persisted=true; reset overlay in that case
    window.addEventListener('pageshow', function (ev) {
        if (ev.persisted) resetOverlay();
    });
})();