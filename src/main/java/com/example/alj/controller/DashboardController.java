package com.example.alj.controller;

import com.example.alj.entity.User;
import com.example.alj.service.ChatService;
import com.example.alj.service.ReminderService;
import com.example.alj.service.UserService;
import lombok.RequiredArgsConstructor;
import org.springframework.security.core.Authentication;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
@RequiredArgsConstructor
public class DashboardController {

    private final UserService userService;
    private final ChatService chatService;
    private final ReminderService reminderService;

    @GetMapping("/")
    public String root() {
        return "redirect:/dashboard";
    }

    @GetMapping("/dashboard")
    public String dashboard(Authentication authentication, Model model) {
        User user = userService.findByUsername(authentication.getName())
                .orElseThrow(() -> new RuntimeException("User not found"));

        model.addAttribute("username", user.getUsername());
        model.addAttribute("role", user.getRole().name());
        model.addAttribute("chatCount", chatService.getChatCount(user));
        model.addAttribute("reminderCount", reminderService.getTotalCount(user));
        model.addAttribute("pendingReminders", reminderService.getPendingCount(user));
        model.addAttribute("recentChats", chatService.getRecentChats(user));
        model.addAttribute("upcomingReminders", reminderService.getUpcomingReminders(user));

        return "dashboard";
    }
}
