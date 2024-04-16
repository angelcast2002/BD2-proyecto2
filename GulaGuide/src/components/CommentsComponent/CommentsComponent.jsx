import React from "react"
import style from "./CommentsComponent.module.css"


/**
 * 
 * Comments debería ser un array con la siguiente estructura:
 * [[nombre: string, comentario: string], [nombre: string, comentario: string], [nombre: string, comentario: string]]
 * Se definirá una variable dummy para simular el comportamiento de la variable comments
 */

const CommentsComponent = ({ comments }) => {

  comments = [["Juan", "Muy buena comida"], ["Pedro", "Muy mal servicio"], ["Maria", "Excelente lugar"], ["Jose Perez", "En realidad no me gustó mucho la comida, los baños estaban algo sucios pero la atención fue excelente. Creo que la mesera estaba coqueteando conmigo. A mi esposa no le gustó mucho. "]]

  return (
    <div className={style.mainContainer}>
      <h2>Comentarios</h2>
      <div className={style.commentsContainer}>
        {comments.map((comment, index) => {
          return (
            <p>
              <strong>{comment[0]}:</strong> {comment[1]}
            </p>
          )
        })}
      </div>
    </div>
  )
}

export default CommentsComponent