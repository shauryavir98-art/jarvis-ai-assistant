package com.example.alj.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class ReminderDto {

    private Long id;

    @NotBlank(message = "Title is required")
    private String title;

    @NotNull(message = "Reminder time is required")
    private LocalDateTime reminderTime;

    private String status;
}
