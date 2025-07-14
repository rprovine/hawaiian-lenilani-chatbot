// Global type declarations
declare global {
  interface Window {
    LeniLaniChatbot?: {
      open: () => void;
      close: () => void;
      isOpen: () => boolean;
    };
    LeniLaniConfig?: {
      position?: 'bottom-right' | 'bottom-left';
      primaryColor?: string;
      greeting?: string;
    };
  }
}

export {};