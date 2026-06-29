package com.example.alj.controller;

import com.example.alj.dto.ReminderDto;
import com.example.alj.entity.User;
import com.example.alj.service.ReminderService;
import com.example.alj.service.UserService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@Controller
@RequiredArgsConstructor
public class ReminderController {

    private final ReminderService reminderService;
    private final UserService userService;

    @GetMapping("/reminders")
    public String remindersPage(Authentication authentication, Model model) {
        User user = getAuthenticatedUser(authentication);
        model.addAttribute("username", user.getUsername());
        model.addAttribute("reminders", reminderService.getAllReminders(user));
        model.addAttribute("pendingCount", reminderService.getPendingCount(user));
        return "reminders";
    }

    @PostMapping("/api/reminders")
    @ResponseBody
    public ResponseEntity<ReminderDto> createReminder(
            @Valid @RequestBody ReminderDto dto,
            Authentication authentication) {

        User user = getAuthenticatedUser(authentication);
        ReminderDto created = reminderService.createReminder(dto, user);
        return ResponseEntity.ok(created);
    }

    @GetMapping("/api/reminders")
    @ResponseBody
    public ResponseEntity<List<ReminderDto>> getAllReminders(Authentication authentication) {
        User user = getAuthenticatedUser(authentication);
        return ResponseEntity.ok(reminderService.getAllReminders(user));
    }

    @PutMapping("/api/reminders/{id}/status")
    @ResponseBody
    public ResponseEntity<ReminderDto> updateStatus(
            @PathVariable Long id,
            @RequestBody Map<String, String> body,
            Authentication authentication) {

        User user = getAuthenticatedUser(authentication);
        ReminderDto updated = reminderService.updateStatus(id, body.get("status"), user);
        return ResponseEntity.ok(updated);
    }

    @DeleteMapping("/api/reminders/{id}")
    @ResponseBody
    public ResponseEntity<Void> deleteReminder(
            @PathVariable Long id,
            Authentication authentication) {

        User user = getAuthenticatedUser(authentication);
        reminderService.deleteReminder(id, user);
        return ResponseEntity.ok().build();
    }

    private User getAuthenticatedUser(Authentication authentication) {
        return userService.findByUsername(authentication.getName())
                .orElseThrow(() -> new RuntimeException("User not found"));
    }
}
