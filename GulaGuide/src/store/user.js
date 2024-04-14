const user = (store) => {
  store.on("@init", () => ({
    user: {
      token: " ",
      role: " ",
      id_user: " ",
    },
  }))
  store.on("user/config", (_, newConfigs) => ({ user: newConfigs }))
}

export default user
