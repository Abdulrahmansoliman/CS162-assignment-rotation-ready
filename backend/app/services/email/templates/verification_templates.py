"""
Verification Email Templates

Templates for verification-related emails (registration, login, etc.)
"""

from app.services.email.templates.template_engine import TemplateEngine


class VerificationTemplates:
    """
    Pre-defined templates for verification emails.
    
    Call register_all() to register these templates with the TemplateEngine.
    """
    
    # Template Names
    REGISTRATION_CODE = 'verification_registration'
    LOGIN_CODE = 'verification_login'
    WELCOME = 'welcome'
    
    @classmethod
    def register_all(cls) -> None:
        """Register all verification templates."""
        cls._register_registration_template()
        cls._register_login_template()
        cls._register_welcome_template()
    
    @classmethod
    def _register_registration_template(cls) -> None:
        """Register the registration verification code template."""
        text_template = """
Hello {name},

Welcome to Rotation Ready! Please use the following verification code to complete your registration:

{code}

This code will expire in {expiry_minutes} minutes.

If you didn't create an account with Rotation Ready, please ignore this email.

Best regards,
The Rotation Ready Team
"""

        html_template = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Verify Your Email</title>
</head>
<body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f5f5f5;">
    <table role="presentation" style="width: 100%; border-collapse: collapse;">
        <tr>
            <td align="center" style="padding: 40px 0;">
                <table role="presentation" style="width: 600px; max-width: 100%; border-collapse: collapse; background-color: #ffffff; border-radius: 12px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                    <!-- Header -->
                    <tr>
                        <td style="padding: 40px 40px 20px; text-align: center; background: linear-gradient(135deg, #cc0000 0%, #ff4444 100%); border-radius: 12px 12px 0 0;">
                            <h1 style="margin: 0; color: #ffffff; font-size: 28px; font-weight: 700;">Rotation Ready</h1>
                        </td>
                    </tr>
                    
                    <!-- Content -->
                    <tr>
                        <td style="padding: 40px;">
                            <h2 style="margin: 0 0 20px; color: #333333; font-size: 22px;">Hello {name}! 👋</h2>
                            <p style="margin: 0 0 20px; color: #666666; font-size: 16px; line-height: 1.6;">
                                Welcome to Rotation Ready! Use the verification code below to complete your registration:
                            </p>
                            
                            <!-- Code Box -->
                            <div style="background-color: #f8f8f8; border: 2px dashed #cc0000; border-radius: 8px; padding: 20px; text-align: center; margin: 30px 0;">
                                <span style="font-family: 'Courier New', monospace; font-size: 32px; font-weight: bold; color: #cc0000; letter-spacing: 6px;">{code}</span>
                            </div>
                            
                            <p style="margin: 0 0 10px; color: #999999; font-size: 14px; text-align: center;">
                                ⏱️ This code expires in <strong>{expiry_minutes} minutes</strong>
                            </p>
                            
                            <hr style="border: none; border-top: 1px solid #eeeeee; margin: 30px 0;">
                            
                            <p style="margin: 0; color: #999999; font-size: 13px; line-height: 1.5;">
                                If you didn't create an account with Rotation Ready, you can safely ignore this email.
                            </p>
                        </td>
                    </tr>
                    
                    <!-- Footer -->
                    <tr>
                        <td style="padding: 20px 40px; background-color: #f8f8f8; border-radius: 0 0 12px 12px; text-align: center;">
                            <p style="margin: 0; color: #999999; font-size: 12px;">
                                © 2024 Rotation Ready. All rights reserved.
                            </p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
"""
        
        TemplateEngine.register(
            cls.REGISTRATION_CODE,
            text_template.strip(),
            html_template.strip()
        )
    
    @classmethod
    def _register_login_template(cls) -> None:
        """Register the login verification code template."""
        text_template = """
Hello {name},

Your Rotation Ready login verification code is:

{code}

This code will expire in {expiry_minutes} minutes.

If you didn't request this code, please secure your account immediately.

Best regards,
The Rotation Ready Team
"""

        html_template = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login Verification Code</title>
</head>
<body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f5f5f5;">
    <table role="presentation" style="width: 100%; border-collapse: collapse;">
        <tr>
            <td align="center" style="padding: 40px 0;">
                <table role="presentation" style="width: 600px; max-width: 100%; border-collapse: collapse; background-color: #ffffff; border-radius: 12px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                    <!-- Header -->
                    <tr>
                        <td style="padding: 40px 40px 20px; text-align: center; background: linear-gradient(135deg, #1d9a5c 0%, #2fb872 100%); border-radius: 12px 12px 0 0;">
                            <h1 style="margin: 0; color: #ffffff; font-size: 28px; font-weight: 700;">Rotation Ready</h1>
                        </td>
                    </tr>
                    
                    <!-- Content -->
                    <tr>
                        <td style="padding: 40px;">
                            <h2 style="margin: 0 0 20px; color: #333333; font-size: 22px;">Welcome back, {name}! 🔐</h2>
                            <p style="margin: 0 0 20px; color: #666666; font-size: 16px; line-height: 1.6;">
                                Use the verification code below to complete your login:
                            </p>
                            
                            <!-- Code Box -->
                            <div style="background-color: #f0fdf4; border: 2px dashed #1d9a5c; border-radius: 8px; padding: 20px; text-align: center; margin: 30px 0;">
                                <span style="font-family: 'Courier New', monospace; font-size: 32px; font-weight: bold; color: #1d9a5c; letter-spacing: 6px;">{code}</span>
                            </div>
                            
                            <p style="margin: 0 0 10px; color: #999999; font-size: 14px; text-align: center;">
                                ⏱️ This code expires in <strong>{expiry_minutes} minutes</strong>
                            </p>
                            
                            <hr style="border: none; border-top: 1px solid #eeeeee; margin: 30px 0;">
                            
                            <p style="margin: 0; color: #999999; font-size: 13px; line-height: 1.5;">
                                ⚠️ If you didn't request this code, please secure your account immediately.
                            </p>
                        </td>
                    </tr>
                    
                    <!-- Footer -->
                    <tr>
                        <td style="padding: 20px 40px; background-color: #f8f8f8; border-radius: 0 0 12px 12px; text-align: center;">
                            <p style="margin: 0; color: #999999; font-size: 12px;">
                                © 2024 Rotation Ready. All rights reserved.
                            </p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
"""
        
        TemplateEngine.register(
            cls.LOGIN_CODE,
            text_template.strip(),
            html_template.strip()
        )
    
    @classmethod
    def _register_welcome_template(cls) -> None:
        """Register the welcome email template."""
        text_template = """
Hello {name},

Welcome to Rotation Ready! 🎉

Your account has been successfully verified and you're all set to explore rotation cities around the world.

Get started by:
- Browsing local recommendations in your rotation city
- Adding your own favorite spots
- Connecting with other rotators

We're excited to have you on board!

Best regards,
The Rotation Ready Team
"""

        html_template = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome to Rotation Ready</title>
</head>
<body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f5f5f5;">
    <table role="presentation" style="width: 100%; border-collapse: collapse;">
        <tr>
            <td align="center" style="padding: 40px 0;">
                <table role="presentation" style="width: 600px; max-width: 100%; border-collapse: collapse; background-color: #ffffff; border-radius: 12px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                    <!-- Header -->
                    <tr>
                        <td style="padding: 40px 40px 20px; text-align: center; background: linear-gradient(135deg, #cc0000 0%, #ff4444 100%); border-radius: 12px 12px 0 0;">
                            <h1 style="margin: 0; color: #ffffff; font-size: 28px; font-weight: 700;">🎉 Welcome to Rotation Ready!</h1>
                        </td>
                    </tr>
                    
                    <!-- Content -->
                    <tr>
                        <td style="padding: 40px;">
                            <h2 style="margin: 0 0 20px; color: #333333; font-size: 22px;">Hello {name}!</h2>
                            <p style="margin: 0 0 20px; color: #666666; font-size: 16px; line-height: 1.6;">
                                Your account has been successfully verified and you're all set to explore rotation cities around the world.
                            </p>
                            
                            <h3 style="margin: 30px 0 15px; color: #333333; font-size: 18px;">Get started by:</h3>
                            <ul style="margin: 0 0 30px; padding-left: 20px; color: #666666; font-size: 15px; line-height: 1.8;">
                                <li>🌍 Browsing local recommendations in your rotation city</li>
                                <li>⭐ Adding your own favorite spots</li>
                                <li>👥 Connecting with other rotators</li>
                            </ul>
                            
                            <p style="margin: 0; color: #666666; font-size: 16px; line-height: 1.6;">
                                We're excited to have you on board!
                            </p>
                        </td>
                    </tr>
                    
                    <!-- Footer -->
                    <tr>
                        <td style="padding: 20px 40px; background-color: #f8f8f8; border-radius: 0 0 12px 12px; text-align: center;">
                            <p style="margin: 0; color: #999999; font-size: 12px;">
                                © 2024 Rotation Ready. All rights reserved.
                            </p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
"""
        
        TemplateEngine.register(
            cls.WELCOME,
            text_template.strip(),
            html_template.strip()
        )
