(function () {
    /* ! access the main Streamlit document from inside the components iframe */
    var doc = window.parent.document;

    function positionFooter() {
        var main   = doc.querySelector('section[data-testid="stMain"]');
        var footer = doc.getElementById('autoblogs-footer');
        if (!main || !footer) return;

        var rect = main.getBoundingClientRect();
        footer.style.left  = rect.left + 'px';
        footer.style.width = rect.width + 'px';
    }

    /* Poll until Streamlit has mounted the main section, then wire observers. */
    function init() {
        var main = doc.querySelector('section[data-testid="stMain"]');
        if (!main) { setTimeout(init, 100); return; }

        positionFooter();

        /* Fires whenever the main panel resizes (sidebar open / close / drag). */
        new ResizeObserver(positionFooter).observe(main);

        /* Fires on browser window resize. */
        window.parent.addEventListener('resize', positionFooter);
    }

    init();
})();
