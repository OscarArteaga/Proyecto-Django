document.addEventListener('DOMContentLoaded', function() {
    let currentIndex = 0;
    const items = document.querySelectorAll('.itemCarrusel');
    const totalItems = items.length;

    function showItem(index) {
        items.forEach((item, i) => {
            item.classList.remove('active', 'previous', 'next');
            if (i === index) {
                item.classList.add('active');
            } else if (i === (index - 1 + totalItems) % totalItems) {
                item.classList.add('previous');
            } else if (i === (index + 1) % totalItems) {
                item.classList.add('next');
            }
        });
    }
    function nextItem() {
        currentIndex = (currentIndex + 1) % totalItems;
        showItem(currentIndex);
    }

    // Cambia al siguiente elemento cada 3 segundos
    setInterval(nextItem, 5000);

    document.querySelector('.flechasCarrusel .prev').addEventListener('click', function() {
        currentIndex = (currentIndex - 1 + totalItems) % totalItems;
        showItem(currentIndex);
    });

    document.querySelector('.flechasCarrusel .next').addEventListener('click', function() {
        currentIndex = (currentIndex + 1) % totalItems;
        showItem(currentIndex);
    });

    document.querySelectorAll('#contePuntos > a').forEach(function(dot) {
        dot.addEventListener('click', function() {
            currentIndex = parseInt(this.getAttribute('data-index'));
            showItem(currentIndex);
        });
    });

    showItem(currentIndex);
});
