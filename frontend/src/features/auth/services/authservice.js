export const authService = {
  async register({ email, cityId, firstName, lastName }) {
    const response = await fetch("/api/v1/auth/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        email,
        city_id: parseInt(cityId),
        first_name: firstName,
        last_name: lastName,
      }),
    })

    if (!response.ok) {
      const data = await response.json()
      throw new Error(data.message || "Registration failed")
    }

    return response.json()
  },

  async verifyRegistration({ email, verificationCode }) {
    const response = await fetch("/api/v1/auth/register/verify", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        email,
        verification_code: verificationCode,
      }),
    })

    if (!response.ok) {
      const data = await response.json()
      throw new Error(data.message || "Invalid verification code")
    }

    return response.json()
  },

  async resendVerificationCode({ email }) {
    const response = await fetch("/api/v1/auth/register/resend-code", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email }),
    })

    if (!response.ok) {
      const data = await response.json()
      throw new Error(data.message || "Failed to resend verification code")
    }

    return response.json()
  },

  async login({ email }) {
    const response = await fetch("/api/v1/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email }),
    })

    if (!response.ok) {
      const data = await response.json()
      throw new Error(data.message || "Login initiation failed")
    }

    return response.json()
  },

  async verifyLogin({ email, verificationCode }) {
    const response = await fetch("/api/v1/auth/login/verify", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        email,
        verification_code: verificationCode,
      }),
    })

    if (!response.ok) {
      const data = await response.json()
      throw new Error(data.message || "Invalid verification code")
    }

    return response.json()
  },
}
