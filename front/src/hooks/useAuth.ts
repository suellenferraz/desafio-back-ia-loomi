import { useState, useEffect, useCallback } from 'react';
import { authService } from '../services/authService';
import type { User, LoginCredentials } from '../types/auth';

interface UseAuthReturn {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (credentials: LoginCredentials) => Promise<void>;
  logout: () => Promise<void>;
  hasRole: (role: string) => boolean;
  hasAnyRole: (roles: string[]) => boolean;
}

export const useAuth = (): UseAuthReturn => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Carregar usuário do localStorage ao montar
  useEffect(() => {
    const loadUser = () => {
      try {
        const currentUser = authService.getCurrentUser();
        setUser(currentUser);
      } catch (error) {
        console.error('Erro ao carregar usuário:', error);
        setUser(null);
      } finally {
        setIsLoading(false);
      }
    };

    loadUser();
  }, []);

  const login = useCallback(async (credentials: LoginCredentials) => {
    setIsLoading(true);
    try {
      const { user } = await authService.login(credentials);
      setUser(user);
    } catch (error: any) {
      throw error;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const logout = useCallback(async () => {
    setIsLoading(true);
    try {
      await authService.logout();
      setUser(null);
    } catch (error) {
      console.error('Erro ao fazer logout:', error);
      // Limpar mesmo se houver erro
      setUser(null);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const hasRole = useCallback((role: string) => {
    return user?.roles.includes(role) || false;
  }, [user]);

  const hasAnyRole = useCallback((roles: string[]) => {
    if (!user) return false;
    return roles.some(role => user.roles.includes(role));
  }, [user]);

  return {
    user,
    isAuthenticated: !!user,
    isLoading,
    login,
    logout,
    hasRole,
    hasAnyRole,
  };
};
