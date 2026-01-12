import type { ReactNode } from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import './ProtectedRoute.css';

interface ProtectedRouteProps {
  children: ReactNode;
  requiredRoles?: string[];
  requireAnyRole?: boolean;
}

export const ProtectedRoute = ({ 
  children, 
  requiredRoles = [],
  requireAnyRole = false 
}: ProtectedRouteProps) => {
  const { isAuthenticated, isLoading, hasRole, hasAnyRole } = useAuth();

  if (isLoading) {
    return (
      <div className="protected-route-loading">
        <div>Carregando...</div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  // Verificar roles se necessário
  if (requiredRoles.length > 0) {
    const hasAccess = requireAnyRole
      ? hasAnyRole(requiredRoles)
      : requiredRoles.every(role => hasRole(role));

    if (!hasAccess) {
      return (
        <div className="protected-route-denied">
          <h1>Acesso Negado</h1>
          <p>Você não tem permissão para acessar esta página.</p>
        </div>
      );
    }
  }

  return <>{children}</>;
};
