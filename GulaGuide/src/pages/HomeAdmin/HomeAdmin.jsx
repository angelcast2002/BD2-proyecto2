import React, { useState } from "react"
import styles from "./HomeAdmin.module.css"
import TextAreaAuto from "../../components/textAreaAutosize/TextAreaAuto"
import Button from "../../components/Button/Button"
import useApi from "../../Hooks/useApi"

const HomeAdmin = () => {
  const handleSend = () => {} // Ya no se usa. 
  const handleTextArea = (e) => {
    setTextArea(e.target.value)
    console.log(e.target.value)
  }
  const handleLogOut = () => {}

  const [textArea, setTextArea] = useState("")
  const [response, setResponse] = useState("")

  const api = useApi()

  
  const sendQuery = async () => {
    const res = await api.handleRequest(
      "GET", 
      "admin/execute_query?query=" + textArea
      )
      const data = await res
      const plainTextData = JSON.stringify(data.data, null, 2) // Convertir a texto plano
      console.log("data", data)
      setResponse(plainTextData)
  }

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
            onChange={handleTextArea}
            minRows={5}
            maxRows={20}
            value={response}
            disabled
          />
        </div>
      </div>
      <div className={styles.buttonsContainer}>
        <Button label="Enviar Consulta" onClick={sendQuery} />
        <Button label="Salir" onChange={handleLogOut} />
      </div>
    </div>
  )
}

export default HomeAdmin
