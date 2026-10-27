(() => {
  'use strict';
  document.querySelectorAll('[data-c4-tabs]').forEach((tablist) => {
    const tabs = Array.from(tablist.querySelectorAll('.c4-tab'));
    const panels = tabs.map((tab) => document.getElementById(tab.getAttribute('aria-controls')));
    if (!tabs.length || panels.some((panel) => !panel)) return;

    // Progressive enhancement: without JavaScript all three views remain readable.
    tablist.setAttribute('role', 'tablist');
    tablist.setAttribute('aria-orientation', 'horizontal');
    const selectTab = (index, focus = false) => {
      tabs.forEach((tab, position) => {
        const selected = position === index;
        tab.setAttribute('aria-selected', String(selected));
        tab.tabIndex = selected ? 0 : -1;
        panels[position].hidden = !selected;
      });
      if (focus) tabs[index].focus();
      // A partially visible tab may already count as focused to the browser.
      // Keep its full label readable in the narrow, horizontally scrollable list.
      if (tablist.clientWidth > 0) {
        const selected = tabs[index].getBoundingClientRect();
        const list = tablist.getBoundingClientRect();
        if (selected.left < list.left + 6) tablist.scrollLeft += selected.left - list.left - 6;
        else if (selected.right > list.right - 6) tablist.scrollLeft += selected.right - list.right + 6;
      }
    };
    tabs.forEach((tab, index) => {
      tab.setAttribute('role', 'tab');
      panels[index].setAttribute('role', 'tabpanel');
      panels[index].setAttribute('aria-labelledby', tab.id);
      panels[index].tabIndex = 0;
      tab.addEventListener('click', () => selectTab(index));
      tab.addEventListener('keydown', (event) => {
        let next = index;
        if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
        else if (event.key === 'ArrowLeft') next = (index - 1 + tabs.length) % tabs.length;
        else if (event.key === 'Home') next = 0;
        else if (event.key === 'End') next = tabs.length - 1;
        else return;
        event.preventDefault();
        selectTab(next, true);
      });
    });
    selectTab(0);
    tablist.hidden = false;
  });
})();
