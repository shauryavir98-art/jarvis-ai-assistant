package com.example.alj.controller;

import com.example.alj.dto.ChatRequestDto;
import com.example.alj.dto.ChatResponseDto;
import com.example.alj.entity.User;
import com.example.alj.service.ChatService;
import com.example.alj.service.UserService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@Controller
@RequiredArgsConstructor
public class ChatController {

    private final ChatService chatService;
    private final UserService userService;

    @GetMapping("/chat")
    public String chatPage(Authentication authentication, Model model) {
        User user = getAuthenticatedUser(authentication);
        model.addAttribute("username", user.getUsername());
        model.addAttribute("chatHistory", chatService.getRecentChats(user));
        return "chat";
    }

    @PostMapping("/api/chat")
    @ResponseBody
    public ResponseEntity<ChatResponseDto> sendMessage(
            @Valid @RequestBody ChatRequestDto request,
            Authentication authentication) {

        User user = getAuthenticatedUser(authentication);
        ChatResponseDto response = chatService.processChat(request, user);
        return ResponseEntity.ok(response);
    }

    @GetMapping("/api/chat/history")
    @ResponseBody
    public ResponseEntity<List<ChatResponseDto>> getChatHistory(Authentication authentication) {
        User user = getAuthenticatedUser(authentication);
        return ResponseEntity.ok(chatService.getChatHistory(user));
    }

    private User getAuthenticatedUser(Authentication authentication) {
        return userService.findByUsername(authentication.getName())
                .orElseThrow(() -> new RuntimeException("User not found"));
    }
}
