package com.example.alj.service;

import com.example.alj.dto.ChatRequestDto;
import com.example.alj.dto.ChatResponseDto;
import com.example.alj.entity.ChatHistory;
import com.example.alj.entity.User;
import com.example.alj.repository.ChatHistoryRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.client.RestTemplate;

import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
@Slf4j
public class ChatService {

    private final ChatHistoryRepository chatHistoryRepository;

    @Value("${jarvis.ai-engine.url:http://localhost:5000}")
    private String aiEngineUrl;

    /**
     * Process a chat question: send to AI engine, save history, return response.
     */
    @Transactional
    public ChatResponseDto processChat(ChatRequestDto request, User user) {
        String aiResponse;

        try {
            RestTemplate restTemplate = new RestTemplate();
            @SuppressWarnings("unchecked")
            Map<String, Object> body = restTemplate.postForObject(
                    aiEngineUrl + "/api/chat",
                    Map.of("question", request.getQuestion()),
                    Map.class
            );
            aiResponse = body != null ? (String) body.get("response") : "No response from AI engine.";
        } catch (Exception e) {
            log.warn("AI engine unavailable, using fallback response: {}", e.getMessage());
            aiResponse = generateFallbackResponse(request.getQuestion());
        }

        ChatHistory chatHistory = ChatHistory.builder()
                .question(request.getQuestion())
                .response(aiResponse)
                .user(user)
                .build();

        chatHistory = chatHistoryRepository.save(chatHistory);

        return ChatResponseDto.builder()
                .id(chatHistory.getId())
                .question(chatHistory.getQuestion())
                .response(chatHistory.getResponse())
                .timestamp(chatHistory.getTimestamp())
                .build();
    }

    /**
     * Get chat history for a user.
     */
    public List<ChatResponseDto> getChatHistory(User user) {
        return chatHistoryRepository.findByUserOrderByTimestampDesc(user)
                .stream()
                .map(ch -> ChatResponseDto.builder()
                        .id(ch.getId())
                        .question(ch.getQuestion())
                        .response(ch.getResponse())
                        .timestamp(ch.getTimestamp())
                        .build())
                .collect(Collectors.toList());
    }

    /**
     * Get recent chat history (top 10) for dashboard.
     */
    public List<ChatResponseDto> getRecentChats(User user) {
        return chatHistoryRepository.findTop10ByUserOrderByTimestampDesc(user)
                .stream()
                .map(ch -> ChatResponseDto.builder()
                        .id(ch.getId())
                        .question(ch.getQuestion())
                        .response(ch.getResponse())
                        .timestamp(ch.getTimestamp())
                        .build())
                .collect(Collectors.toList());
    }

    public long getChatCount(User user) {
        return chatHistoryRepository.countByUser(user);
    }

    /**
     * Fallback response when the Python AI engine is not available.
     */
    private String generateFallbackResponse(String question) {
        String q = question.toLowerCase().trim();

        if (q.contains("hello") || q.contains("hi") || q.contains("hey")) {
            return "Hello! I'm JARVIS, your AI assistant. The AI engine is currently offline, but I can still help with basic queries. How can I assist you?";
        }
        if (q.contains("time")) {
            return "The current server time is: " + java.time.LocalDateTime.now().format(
                    java.time.format.DateTimeFormatter.ofPattern("hh:mm a, EEEE, MMMM dd, yyyy"));
        }
        if (q.contains("who are you") || q.contains("what are you")) {
            return "I am JARVIS — Just A Rather Very Intelligent System. I'm an AI assistant built with Spring Boot and Python, designed to help you with tasks, answer questions, and manage reminders.";
        }
        if (q.contains("help")) {
            return "I can help you with:\n• Answering questions (when AI engine is online)\n• Managing reminders\n• Opening websites and applications\n• General conversation\n\nPlease start the Python AI engine for full functionality.";
        }

        return "I received your message: \"" + question + "\". The AI engine is currently offline. Please start it with `python main.py` in the ai-engine directory for full AI capabilities.";
    }
}
