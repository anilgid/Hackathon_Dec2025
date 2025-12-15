import html

class SecurityService:
    @staticmethod
    def sanitize_input(user_input: str) -> str:
        """
        Sanitizes user input to prevent basic XSS and injection attacks.
        Currently primarily escapes HTML characters.
        """
        if not user_input:
            return ""
        
        # Basic HTML escaping
        sanitized = html.escape(user_input)
        
        # In a real-world scenario, we might want to use a library like 'bleach'
        # for more sophisticated sanitization if we were allowing some HTML.
        # For now, we strictly escape everything.
        
        return sanitized
