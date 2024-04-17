import React, { useState } from "react"
import styles from "./HomeAdmin.module.css"
import TextAreaAuto from "../../components/textAreaAutosize/TextAreaAuto"
import Button from "../../components/Button/Button"
import useApi from "../../Hooks/useApi"

const HomeAdmin = () => {
  const handleSend = () => {}
  const handleTextArea = (e) => {
    setTextArea(e.target.value)
  }
  const handleLogOut = () => {}

  const [textArea, setTextArea] = useState("")
  const [response, setResponse] = useState("")

  return (
    <div className={styles.container}>
      <div className={styles.inputContainer}>
        <div className={styles.subCampoContainer}>
          <h1>Consulta</h1>
          <TextAreaAuto
            name="textArea"
            type="text"
            placeholder="Escribe aquí tu consulta..."
            onChange={handleTextArea}
            minRows={5}
            maxRows={10}
            value={textArea}
          />
        </div>
        <div className={styles.subCampoContainer}>
          <h1>Respuesta</h1>
          <TextAreaAuto
            name="textArea"
            type="text"
            placeholder="Escribe aquí tu consulta..."
            onChange={handleTextArea}
            minRows={5}
            maxRows={10}
            value={response}
            disabled
          />
        </div>
      </div>
      <div className={styles.buttonsContainer}>
        <Button label="Enviar Consulta" onChange={handleSend} />
        <Button label="Salir" onChange={handleLogOut} />
      </div>
    </div>
  )
}

export default HomeAdmin
