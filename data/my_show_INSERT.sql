INSERT INTO public.series ("name", photo, rating, status, review)
VALUES (%s, %s, %s, %s, %s)
RETURNING *;

--('Игра престолов','https://www.kinopoisk.ru/film/464963/posters/',1,'watching'::public."seriesstatus",'None'),
--('Во все тяжкие','https://www.kinopoisk.ru/film/464963/posters/',9,'watching'::public."seriesstatus",'None'),
--('Гангстерленд','https://www.kinopoisk.ru/film/464963/posters/',5,'watching'::public."seriesstatus",'None');
--