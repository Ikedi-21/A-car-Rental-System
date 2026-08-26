// Admin panel interactions — sidebar toggle on mobile, plus anything
// admin-specific goes here rather than main.js, since none of this
// applies to the public-facing pages.

document.addEventListener('DOMContentLoaded', function () {

    // Mobile sidebar toggle — the sidebar is fixed off-screen by default
    // on small viewports (see admin.css), this just slides it in/out
    const toggleBtn = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('adminSidebar');

    if (toggleBtn && sidebar) {
        toggleBtn.addEventListener('click', function () {
            sidebar.classList.toggle('open');
        });

        // clicking outside the open sidebar closes it again — without this
        // it just stays open until you tap the toggle a second time, which
        // feels broken on a phone
        document.addEventListener('click', function (e) {
            const clickedInsideSidebar = sidebar.contains(e.target);
            const clickedToggle = toggleBtn.contains(e.target);
            if (!clickedInsideSidebar && !clickedToggle) {
                sidebar.classList.remove('open');
            }
        });
    }

});