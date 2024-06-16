var faqElements = document.querySelectorAll('.faq-element');

faqElements.forEach(function (faqElement) {
    faqElement.addEventListener('click', function () {
        var content = this.querySelector('.faq-question-content');
        var icon = this.querySelector('.fa-icon');
        content.classList.toggle('show');
        icon.classList.toggle('rotate');


        // Füge diese Bedingung hinzu, um die Opazität und Höhe zu steuern
        if (content.classList.contains('show')) {
            setTimeout(function () {
                content.style.opacity = 1;
                content.style.height = content.scrollHeight + 'px';
            }, 10);
        } else {
            content.style.opacity = 0;
            content.style.height = 0;
        }
    });
});