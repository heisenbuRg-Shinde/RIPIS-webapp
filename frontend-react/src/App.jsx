import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import Login from './components/Login';
import Register from './components/Register';
import Reasoning from './components/Reasoning';
import ProtectedRoute from './components/ProtectedRoute';

function AppRoutes() {
    const { isAuthenticated, loading } = useAuth();

    if (loading) {
        return (
            <div className="loading-state" style={{ minHeight: '100vh' }}>
                <div className="loader"></div>
                <p>Loading RIPIS...</p>
            </div>
        );
    }

    return (
        <Routes>
            <Route
                path="/login"
                element={isAuthenticated ? <Navigate to="/" replace /> : <Login />}
            />
            <Route
                path="/register"
                element={isAuthenticated ? <Navigate to="/" replace /> : <Register />}
            />
            <Route
                path="/"
                element={
                    <ProtectedRoute>
                        <Reasoning />
                    </ProtectedRoute>
                }
            />
            <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
    );
}

function App() {
    return (
        <BrowserRouter>
            <AuthProvider>
                <AppRoutes />
            </AuthProvider>
        </BrowserRouter>
    );
}

export default App;
