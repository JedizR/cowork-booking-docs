# Traceability

Every Decided or Stakeholder-clarified rule maps to passing test node IDs or to a manual check (steps and result). Node IDs name the junit report they come from: `purchase`, `payment`, `access` (each service's own suite) or `e2e` (the integration suite in `integration/e2e`, run against the three services). The reports are committed in `integration/reports/`, so `scripts/check_docs.py` verifies every cited node exists and passed, without Docker.

Final runs, 2026-10-01: purchase 39 passed, payment 26 passed, access 31 passed, e2e 24 passed (run twice against the same stack).

| Rule | Status | Evidence |
|---|---|---|
| PUR-R01 | Decided (D15, D16) | `purchase:tests/test_purchase.py::test_pur_r01_register_rejects_duplicate_email` |
| PUR-R02 | Decided (D15, D16) | `purchase:tests/test_purchase.py::test_pur_r02_login_has_one_uniform_error` |
| PUR-R03 | Decided (D15) | `e2e:e2e/test_booking.py::test_decline_keeps_purchase_login_pur_r03`, `purchase:tests/test_purchase.py::test_pur_r03_cookie_is_httponly_and_samesite_lax`, `purchase:tests/test_purchase.py::test_pur_r03_session_ends_12_hours_after_login` |
| PUR-R04 | Decided (D15) | `purchase:tests/test_purchase.py::test_pur_r04_operator_promoted_by_operator_email` |
| PUR-R05 | Decided (D15, D17) | `e2e:e2e/test_repeats.py::test_non_owner_gets_404_pur_r05`, `purchase:tests/test_purchase.py::test_pur_r05_anonymous_booking_goes_to_login_and_keeps_the_page`, `purchase:tests/test_purchase.py::test_pur_r05_non_owner_gets_404` |
| PUR-R06 | Decided (D15, D17) | `purchase:tests/test_purchase.py::test_pur_r06_operator_pages_are_404_for_members` |
| PUR-R07 | Decided (D2) | `purchase:tests/test_purchase.py::test_pur_r07_json_time_needs_an_offset` |
| PUR-R08 | Decided (D3) | `purchase:tests/test_purchase.py::test_pur_r08_r09_shape_checks` |
| PUR-R09 | Decided (D4) | `purchase:tests/test_purchase.py::test_pur_r08_r09_shape_checks` |
| PUR-R10 | Decided (D5) | `purchase:tests/test_purchase.py::test_pur_r10_notice_and_horizon` |
| PUR-R11 | Decided (D6) | `purchase:tests/test_purchase.py::test_pur_r11_r12_adjacent_allowed_overlap_taken` |
| PUR-R12 | Decided (D11) | `purchase:tests/test_purchase.py::test_pur_r11_r12_adjacent_allowed_overlap_taken` |
| PUR-R13 | Decided (D4, D11) | `purchase:tests/test_purchase.py::test_pur_r13_grid_reasons` |
| PUR-R14 | Decided (D7) | manual: live journey verified 2026-10-01: POST /api/bookings for Meeting Room A (capacity 6) with party_size 7 gives 400 invalid_request. |
| PUR-R15 | Decided (D7, D9) | `purchase:tests/test_purchase.py::test_pur_r15_space_values_checked` |
| PUR-R16 | Decided (D23) | `purchase:tests/test_purchase.py::test_pur_r16_archive_waits_for_upcoming_bookings` |
| PUR-R17 | Stakeholder-clarified (course instructor, class rules PR #14 at 25ca71e) | `purchase:tests/test_purchase.py::test_pur_r17_price_fixed_at_creation` |
| PUR-R18 | Decided (D1) | `purchase:tests/test_purchase.py::test_pur_r18_money_shown_as_thb` |
| PUR-R19 | Decided (D10, D8) | `purchase:tests/test_purchase.py::test_pur_r19_r20_plan_skips_payment` |
| PUR-R20 | Decided (D10, D20) | `e2e:e2e/test_booking.py::test_free_skips_payment_pur_r20`, `e2e:e2e/test_booking.py::test_plan_skips_payment_pur_r20`, `purchase:tests/test_purchase.py::test_pur_r19_r20_plan_skips_payment`, `purchase:tests/test_purchase.py::test_pur_r20_free_space_confirms_at_once` |
| PUR-R21 | Decided (D11) | `e2e:e2e/test_repeats.py::test_double_submit_resumes_hold_pur_r21`, `purchase:tests/test_purchase.py::test_pur_r21_r23_double_submit_resumes_hold_and_session_ends_before_hold` |
| PUR-R22 | Decided (D11, D13) | manual: live journey verified 2026-10-01: two Members POST /api/bookings for the same Board Room slot concurrently; answers [201, 409] (partial EXCLUDE guard). |
| PUR-R23 | Decided (D12) | `purchase:tests/test_purchase.py::test_pur_r21_r23_double_submit_resumes_hold_and_session_ends_before_hold`, `purchase:tests/test_purchase.py::test_pur_r23_payment_unreachable_keeps_hold_without_session` |
| PUR-R24 | Decided (D13) | `e2e:e2e/test_booking.py::test_hold_expiry_frees_slot_pur_r24`, `e2e:e2e/test_booking.py::test_lost_redirect_reconciled_on_next_read_pur_r24`, `purchase:tests/test_purchase.py::test_pur_r24_hold_expiry_frees_the_slot`, `purchase:tests/test_purchase.py::test_pur_r24_lost_redirect_confirmed_on_next_read` |
| PUR-R25 | Decided (D14) | `e2e:e2e/test_booking.py::test_happy_path_pur_r25_confirm_and_grant`, `e2e:e2e/test_booking.py::test_lost_redirect_reconciled_after_hold_lapsed_pur_r25`, `purchase:tests/test_purchase.py::test_pur_r25_amount_mismatch_cancels_and_refunds_in_full` |
| PUR-R26 | Decided (D20) | `purchase:tests/test_purchase.py::test_pur_r26_grant_pending_while_access_down_then_retried` |
| PUR-R27 | Decided (D21) | `e2e:e2e/test_checkin.py::test_checkin_window_axs_r13` (Purchase sends [start, end); the kiosk answers not_open_yet, ok, closed at the edges) |
| PUR-R28 | Decided (D11, D18; Disputes decided in M1, row 7) | `e2e:e2e/test_cancel.py::test_member_cancel_24h_or_more_full_refund_pur_r30`, `purchase:tests/test_purchase.py::test_pur_r30_operator_cancel_always_refunds_in_full` (a cancelled booking stays readable; nothing is deleted) |
| PUR-R29 | Decided (D22) | `purchase:tests/test_purchase.py::test_pur_r29_r39_reference_format_and_one_hold_per_member` |
| PUR-R30 | Decided (D18) | `e2e:e2e/test_cancel.py::test_member_cancel_24h_or_more_full_refund_pur_r30`, `e2e:e2e/test_cancel.py::test_member_cancel_under_24h_no_refund_pur_r30`, `e2e:e2e/test_cancel.py::test_operator_cancel_always_full_refund_pur_r30`, `purchase:tests/test_purchase.py::test_pur_r30_member_cancel_under_24h_refunds_nothing`, `purchase:tests/test_purchase.py::test_pur_r30_operator_cancel_always_refunds_in_full`, `purchase:tests/test_purchase.py::test_pur_r30_r32_member_cancel_24h_ahead_refunds_in_full`, `purchase:tests/test_purchase.py::test_pur_r30_refund_dropped_since_screen_asks_again` |
| PUR-R31 | Decided (D13, D18) | `e2e:e2e/test_cancel.py::test_held_cancel_racing_payment_form_pur_r31`, `e2e:e2e/test_cancel.py::test_held_cancel_racing_payment_json_pur_r31`, `purchase:tests/test_purchase.py::test_pur_r31_held_cancel_racing_payment_refunds`, `purchase:tests/test_purchase.py::test_pur_r31_held_cancel_unpaid_and_payment_unreachable` |
| PUR-R32 | Decided (D19) | `purchase:tests/test_purchase.py::test_pur_r30_r32_member_cancel_24h_ahead_refunds_in_full` |
| PUR-R33 | Decided (D19) | `e2e:e2e/test_cancel.py::test_refund_failure_card_operator_retry_pur_r33`, `purchase:tests/test_purchase.py::test_pur_r33_only_operator_starts_the_next_refund_attempt` |
| PUR-R34 | Decided (D24) | `purchase:tests/test_purchase.py::test_pur_r34_dashboard_markers` |
| PUR-R35 | Decided (D13, D28) | manual: source inspected 2026-10-01: outbound HTTP exists only in payment_client.py and access_client.py, every call passes timeout=5 (grep); Payment and Access import no HTTP client. |
| PUR-R36 | Decided (D28) | `purchase:tests/test_purchase.py::test_pur_r36_url_text_is_never_shown` |
| PUR-R37 | Decided (D15) | `purchase:tests/test_purchase.py::test_pur_r37_logout_is_a_post` |
| PUR-R38 | Decided (D27) | `purchase:tests/test_purchase.py::test_pur_r38_test_clock_404_unless_enabled` |
| PUR-R39 | Decided (D11) | `purchase:tests/test_purchase.py::test_pur_r29_r39_reference_format_and_one_hold_per_member` |
| PUR-R40 | Decided (D11, D12) | `purchase:tests/test_purchase.py::test_pur_r40_no_resume_after_the_payment_deadline` |
| PMT-R01 | Decided (D13; ADR-0004 (Purchase-only callers), no webhooks) | `payment:tests/test_payment.py::test_pmt_r01_missing_wrong_or_basic_token_gets_401_before_validation`, `payment:tests/test_payment.py::test_pmt_r01_r17_r19_start_refuses_missing_or_weak_secrets` |
| PMT-R02 | Decided (D1) | `payment:tests/test_payment.py::test_pmt_r02_amount_of_exactly_thb_10_is_accepted`, `payment:tests/test_payment.py::test_pmt_r02_invalid_fields_get_400_naming_the_field`, `payment:tests/test_payment.py::test_pmt_r02_valid_request_creates_open_session_with_128_bit_id` |
| PMT-R03 | Decided (D11) | `e2e:e2e/test_repeats.py::test_repeat_payment_session_pmt_r03`, `payment:tests/test_payment.py::test_pmt_r03_repeat_returns_stored_session_and_other_amount_gets_409` |
| PMT-R04 | Decided (D8) | `payment:tests/test_payment.py::test_pmt_r04_amount_is_shown_and_collected_as_given` |
| PMT-R05 | Decided (D12) | `payment:tests/test_payment.py::test_pmt_r05_session_reads_expired_from_expires_at_but_paid_stays_paid` |
| PMT-R06 | Decided (D18) | `payment:tests/test_payment.py::test_pmt_r06_expire_after_payment_returns_paid`, `payment:tests/test_payment.py::test_pmt_r06_expire_open_session_then_pay_is_refused` |
| PMT-R07 | Decided (D12) | `payment:tests/test_payment.py::test_pmt_r07_hosted_page_shows_amount_countdown_banner_and_ignores_query` |
| PMT-R08 | Decided (D27; ADR-0018 (mock checkout and test cards)) | `payment:tests/test_payment.py::test_pmt_r08_card_field_errors_are_flashed_and_store_nothing` |
| PMT-R09 | Decided (ADR-0018 (mock checkout and test cards)) | `payment:tests/test_payment.py::test_pmt_r09_r10_test_cards_decide_outcome_and_decline_keeps_session_open` |
| PMT-R10 | Decided (D12) | `e2e:e2e/test_booking.py::test_decline_then_retry_pmt_r10`, `payment:tests/test_payment.py::test_pmt_r09_r10_test_cards_decide_outcome_and_decline_keeps_session_open` |
| PMT-R11 | Decided (D12) | `payment:tests/test_payment.py::test_pmt_r11_attempt_one_second_before_expiry_is_accepted`, `payment:tests/test_payment.py::test_pmt_r11_no_attempt_at_or_after_expires_at` |
| PMT-R12 | Decided (D28) | `e2e:e2e/test_repeats.py::test_pay_twice_charges_once_pmt_r12`, `payment:tests/test_payment.py::test_pmt_r12_double_click_on_two_workers_charges_once`, `payment:tests/test_payment.py::test_pmt_r12_pay_on_complete_session_stores_no_attempt` |
| PMT-R13 | Decided (D28; ADR-0020 (card data handling)) | `payment:tests/test_payment.py::test_pmt_r13_only_brand_and_last4_are_stored` |
| PMT-R14 | Decided (D19) | `e2e:e2e/test_repeats.py::test_cancel_twice_refunds_once_pmt_r14`, `payment:tests/test_payment.py::test_pmt_r14_identical_refunds_together_get_one_201_and_one_200`, `payment:tests/test_payment.py::test_pmt_r14_refund_repeat_returns_stored_result_and_conflicts_get_409` |
| PMT-R15 | Decided (D19) | `payment:tests/test_payment.py::test_pmt_r15_refunds_never_exceed_collected` |
| PMT-R16 | Decided (D19) | `payment:tests/test_payment.py::test_pmt_r16_card_5126_first_refund_fails_then_retry_succeeds` |
| PMT-R17 | Decided (D25; ADR-0019 (service authentication)) | `payment:tests/test_payment.py::test_pmt_r01_r17_r19_start_refuses_missing_or_weak_secrets`, `payment:tests/test_payment.py::test_pmt_r17_operator_page_needs_the_password`, `payment:tests/test_payment.py::test_pmt_r17_operator_totals_and_commission_rounding` |
| PMT-R18 | Decided (D13) | manual: source inspected 2026-10-01: no Payment module imports requests or any HTTP client (grep over *.py, tests excluded). |
| PMT-R19 | Decided (D15) | `payment:tests/test_payment.py::test_pmt_r01_r17_r19_start_refuses_missing_or_weak_secrets`, `payment:tests/test_payment.py::test_pmt_r19_flash_cookie_is_httponly_lax_and_holds_no_card_data` |
| PMT-R20 | Decided (D27) | `payment:tests/test_payment.py::test_pmt_r20_test_clock_is_404_unless_enabled_and_rejects_naive_time` |
| AXS-R01 | Decided (D20) | `access:tests/test_access.py::test_axs_r01_issue_returns_201_with_code_and_url`, `access:tests/test_access.py::test_axs_r01_repeat_returns_stored_grant_unchanged`, `e2e:e2e/test_repeats.py::test_repeat_grant_same_code_axs_r01` |
| AXS-R02 | Decided (D19, D20) | `access:tests/test_access.py::test_axs_r02_revoke_unknown_stores_tombstone_and_issue_gives_nothing` |
| AXS-R03 | Decided (D2, D21) | `access:tests/test_access.py::test_axs_r03_invalid_request_400_names_field_stores_nothing[booking_reference-7KQ2M9-booking_reference must be BK- and 6 symbols]`, `access:tests/test_access.py::test_axs_r03_invalid_request_400_names_field_stores_nothing[member_ref--member_ref is required]`, `access:tests/test_access.py::test_axs_r03_invalid_request_400_names_field_stores_nothing[space_id-2147483648-space_id is out of range]`, `access:tests/test_access.py::test_axs_r03_invalid_request_400_names_field_stores_nothing[space_name--space_name is required]`, `access:tests/test_access.py::test_axs_r03_invalid_request_400_names_field_stores_nothing[valid_from-2026-10-07T09:00:00-valid_from needs a UTC offset]`, `access:tests/test_access.py::test_axs_r03_invalid_request_400_names_field_stores_nothing[valid_until-2026-10-07T09:00:00+07:00-valid_until must be after valid_from]` |
| AXS-R04 | Decided (D19, D20; ADR-0004 (Purchase-only callers), no webhooks) | `access:tests/test_access.py::test_axs_r04_missing_or_wrong_token_401_before_validation`, `access:tests/test_access.py::test_axs_r04_r11_refuse_to_start_on_weak_secret[ACCESS_API_TOKEN--ACCESS_API_TOKEN is required]`, `access:tests/test_access.py::test_axs_r04_r11_refuse_to_start_on_weak_secret[ACCESS_API_TOKEN-short-ACCESS_API_TOKEN must be at least 32 characters]`, `access:tests/test_access.py::test_axs_r04_r11_refuse_to_start_on_weak_secret[STAFF_PASSWORD-xxxxxxxxxxx-STAFF_PASSWORD must be at least 12 characters]` |
| AXS-R05 | Decided (D20, D22) | `access:tests/test_access.py::test_axs_r05_code_issued_once_and_reused_everywhere` |
| AXS-R06 | Decided (D22) | `access:tests/test_access.py::test_axs_r06_code_alphabet_never_starts_with_bk`, `access:tests/test_access.py::test_axs_r06_collision_draws_again` |
| AXS-R07 | Decided (D22) | `access:tests/test_access.py::test_axs_r07_qr_encodes_exactly_the_code` |
| AXS-R08 | Decided (D22) | `access:tests/test_access.py::test_axs_r08_booking_reference_is_unknown_code`, `e2e:e2e/test_checkin.py::test_checkin_unknown_code_and_booking_reference_axs_r08` |
| AXS-R09 | Decided (D17) | `access:tests/test_access.py::test_axs_r09_ticket_is_view_only_bearer_link` |
| AXS-R10 | Decided (D17, D21) | `access:tests/test_access.py::test_axs_r10_badge_follows_state_and_clock` |
| AXS-R11 | Decided (D15, D21; ADR-0019 (service authentication)) | `access:tests/test_access.py::test_axs_r04_r11_refuse_to_start_on_weak_secret[ACCESS_API_TOKEN--ACCESS_API_TOKEN is required]`, `access:tests/test_access.py::test_axs_r04_r11_refuse_to_start_on_weak_secret[ACCESS_API_TOKEN-short-ACCESS_API_TOKEN must be at least 32 characters]`, `access:tests/test_access.py::test_axs_r04_r11_refuse_to_start_on_weak_secret[STAFF_PASSWORD-xxxxxxxxxxx-STAFF_PASSWORD must be at least 12 characters]`, `access:tests/test_access.py::test_axs_r11_kiosk_needs_staff_password`, `access:tests/test_access.py::test_axs_r11_scan_without_room_refused_and_unknown_room` |
| AXS-R12 | Decided (D22) | `access:tests/test_access.py::test_axs_r12_r13_normalised_code_opens_inside_window_and_reentry` |
| AXS-R13 | Decided (D21) | `access:tests/test_access.py::test_axs_r12_r13_normalised_code_opens_inside_window_and_reentry`, `access:tests/test_access.py::test_axs_r13_window_edges`, `e2e:e2e/test_checkin.py::test_checkin_window_axs_r13` |
| AXS-R14 | Decided (D21) | `access:tests/test_access.py::test_axs_r14_order_revoked_before_wrong_room`, `e2e:e2e/test_checkin.py::test_checkin_revoked_axs_r14`, `e2e:e2e/test_checkin.py::test_checkin_wrong_room_axs_r14` |
| AXS-R15 | Decided (D21, D27) | `access:tests/test_access.py::test_axs_r15_every_scan_logged_last_10_masked` |
| AXS-R16 | Decided (D19, D21) | `access:tests/test_access.py::test_axs_r16_condition_derived_no_show_and_expired`, `access:tests/test_access.py::test_axs_r16_first_ok_scan_checks_in_and_revoke_from_checked_in` |
| AXS-R17 | Decided (D19) | `access:tests/test_access.py::test_axs_r17_revoke_idempotent_keeps_revoked_at` |
| AXS-R18 | Decided (D15) | `access:tests/test_access.py::test_axs_r18_cookie_flags_and_seed_secret_refused` |
| AXS-R19 | Decided (D27) | `access:tests/test_access.py::test_axs_r19_test_clock_off_unless_flag_true` |
