package com.example.alj.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class ChatResponseDto {

    private Long id;
    private String question;
    private String response;
    private LocalDateTime timestamp;
}
