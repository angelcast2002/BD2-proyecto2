import React from "react"
import style from "./CommentsComponent.module.css"


/**
 * 
 * Comments debería ser un array con la siguiente estructura:
 * [[nombre: string, comentario: string], [nombre: string, comentario: string], [nombre: string, comentario: string]]
 * Se definirá una variable dummy para simular el comportamiento de la variable comments
 */

const CommentsComponent = ({ comments }) => {

  /**
   * comments es un array de diccionarios. 
   * Comments vendrá de la siguiente forma:
   * [[nombre: string, apellido: string, comentario: string, dishes: [dish1, dish2...] rating: number, total: number] ...
   * Haz un map de comments para mostrar los comentarios en la página.
  */

  return (
    <div className={style.mainContainer}>
      <h2>Comentarios</h2>
      <div className={style.commentsContainer}>
        {comments?.map((comment, index) => (
          <div key={index}>
            <h3>{comment.name + " " + comment.lastname + ": " + comment.comment}</h3>
            <p> Rating dado: {comment.rating} | Total consumido: {comment.total}</p>
            <br />
          </div>
        ))}
      </div>
    </div>
  );
}

export default CommentsComponent