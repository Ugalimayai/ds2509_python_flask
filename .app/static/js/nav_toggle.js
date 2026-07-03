const toggle = document.querySelector('.nav-toggle');
  const navList = document.querySelector('.nav-list');

  toggle.addEventListener('click', () => {
    const expanded = toggle.getAttribute('aria-expanded') === 'true';
    toggle.setAttribute('aria-expanded', !expanded);
    navList.classList.toggle('open');
    toggle.innerHTML = expanded ? '<i class="bi bi-list"></i>' : '<i class="bi bi-x-lg"></i>';
  });
  