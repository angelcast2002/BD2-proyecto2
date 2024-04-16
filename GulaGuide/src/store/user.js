const user = (store) => {
  store.on("@init", () => ({
    user: {
      role: " ",
      id_user: " ",
    },
  }))
  store.on("user/config", (_, newConfigs) => ({ user: newConfigs }))
}

export default user
