export function validateNumber(event) {
    const value = event.target.value;
    event.target.value = value.replace(/\D/g, '');
  }

  export function validateTextOnly(event) {
    const value = event.target.value;
    event.target.value = value.replace(/[^a-zA-ZÀ-ÿ\s'-]/g, '');
  }
  
  export function isValidEmail(email) {
    const regex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return regex.test(email.trim());
  }
  