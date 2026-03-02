#include <iostream>
#include <fstream>
#include <string>
#include <map>
#include <regex>

int main() {
    std::map<std::string, int> historialScores;
    std::ifstream BaseD("memory_agent.txt"); 
    std::string linea, bloqueFecha;
    
    std::regex regDate("<(\\d{2}/\\d{2}/\\d{4} \\d{2}:\\d{2}:\\d{2})>");
    std::regex regScore("<Score>\\s*(\\d+)");

    if (BaseD.is_open()) {
        while (getline(BaseD, linea)) {
            std::smatch match;
            
            if (std::regex_search(linea, match, regDate)) {
                bloqueFecha = match[1]; 
            }
            
            if (std::regex_search(linea, match, regScore)) {
                int valorScore = std::stoi(match[1]);
                historialScores[bloqueFecha] = valorScore; 
            }
        }
        BaseD.close();
    } else {
        std::cout << "No se pudo abrir memory_agent.txt. Verifica que el archivo exista." << std::endl;
        return 1;
    }

    // --- ANÁLISIS DE MEMORIA ---
    std::cout << "--- EVOLUCION DE LA IA (Orden Cronologico) ---" << std::endl;
    
    int primerScore = -1;
    int ultimoScore = -1;

    for (auto it = historialScores.begin(); it != historialScores.end(); ++it) {
        std::string date = it->first;
        int AI_score = it->second;

        if (primerScore == -1) primerScore = AI_score;
        ultimoScore = AI_score;

        std::cout << "[" << date << "] -> Score: " << AI_score << std::endl;
    }

    // Lógica de "Entrenamiento"
    std::cout << "\n--- RESUMEN ---" << std::endl;
    if (primerScore != -1) {
        if (ultimoScore > primerScore) {
            std::cout << "Resultado: La IA esta aprendiendo positivamente (+ " << ultimoScore - primerScore << " pts)" << std::endl;
        } else if (ultimoScore < primerScore) {
            std::cout << "Resultado: El rendimiento ha bajado (" << ultimoScore - primerScore << " pts). Requiere ajuste de prompts." << std::endl;
        } else {
            std::cout << "Resultado: El rendimiento es estable." << std::endl;
        }
    } else {
        std::cout << "No se encontraron datos para analizar." << std::endl;
    }

    return 0;
}