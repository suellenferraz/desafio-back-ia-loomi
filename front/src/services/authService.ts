import { backApi } from './api';
import type { User, LoginCredentials } from '../types/auth';

const AUTH_TOKEN_KEY = 'auth_token';
const USER_KEY = 'user';

export const authService = {
  /**
   * Realiza login e armazena token e usuário
   */
  async login(credentials: LoginCredentials): Promise<{ user: User; token: string }> {
    try {
      const response = await backApi.post<{ user: User; token: string }>('/api/v1/account/login', credentials);
      const { user, token } = response.data;
      
      // Armazenar token e usuário
      localStorage.setItem(AUTH_TOKEN_KEY, token);
      localStorage.setItem(USER_KEY, JSON.stringify(user));
      
      return { user, token };
    } catch (error: any) {
      throw new Error(error.message || 'Erro ao fazer login');
    }
  },

  /**
   * Realiza logout
   */
  async logout(): Promise<void> {
    try {
      await backApi.delete('/api/v1/account/logout');
    } catch (error) {
      // Continuar mesmo se houver erro no backend
      console.error('Erro ao fazer logout no backend:', error);
    } finally {
      // Sempre limpar dados locais
      localStorage.removeItem(AUTH_TOKEN_KEY);
      localStorage.removeItem(USER_KEY);
    }
  },

  /**
   * Obtém usuário atual do localStorage
   */
  getCurrentUser(): User | null {
    const userStr = localStorage.getItem(USER_KEY);
    if (!userStr) return null;
    
    try {
      return JSON.parse(userStr);
    } catch {
      return null;
    }
  },

  /**
   * Obtém token atual do localStorage
   */
  getToken(): string | null {
    return localStorage.getItem(AUTH_TOKEN_KEY);
  },

  /**
   * Verifica se está autenticado
   */
  isAuthenticated(): boolean {
    return !!this.getToken() && !!this.getCurrentUser();
  },

  /**
   * Verifica se usuário tem role específica
   */
  hasRole(role: string): boolean {
    const user = this.getCurrentUser();
    if (!user) return false;
    return user.roles.includes(role);
  },

  /**
   * Verifica se usuário tem uma das roles
   */
  hasAnyRole(roles: string[]): boolean {
    const user = this.getCurrentUser();
    if (!user) return false;
    return roles.some(role => user.roles.includes(role));
  },

};
