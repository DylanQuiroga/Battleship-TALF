document.addEventListener("visibilitychange", function() {
    if (document.visibilityState === 'hidden') {
        document.title = "¡Ven aqui soldado 😡!";
    } else {
        document.title = "Instrucciones";
    }
});