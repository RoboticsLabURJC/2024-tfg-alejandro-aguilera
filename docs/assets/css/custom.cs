/* Aumenta el ancho del contenido principal */
.page__content,
.page__hero--overlay .page__title,
.archive__item,
.page__meta,
.layout--single {
  max-width: 1200px !important; /* Puedes aumentar más si quieres */
  margin-left: auto;
  margin-right: auto;
}

/* Mejora visual en pantallas grandes */
@media (min-width: 1200px) {
  .page {
    max-width: 1400px !important;
  }
}

